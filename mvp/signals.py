from django.db.models.signals import post_delete, post_save, pre_save
from django.db.models import Sum
from django.dispatch import receiver
from .models import Conseil, License, Contract, Invite
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# @receiver(post_delete, sender=Company)
# def auto_delete_ceo_with_company(sender, instance, **kwargs):
#     instance.manager.delete()


def UpdateContractPrice(contract):
    contract.price = 0
    licenses_price = contract.license_set.aggregate(Sum('price'))
    contract.price += licenses_price['price__sum'] or 0
    conseils_price = contract.conseil_set.aggregate(Sum('price'))
    contract.price += conseils_price['price__sum'] or 0
    contract.save()


def UpdateEndDate(instance):
    instance.end_date = instance.start_date + relativedelta(months=+instance.duration)


@receiver(pre_save, sender=Contract)
def UpdateContractEndDate(sender, instance, **kwargs):
    UpdateEndDate(instance)


@receiver(pre_save, sender=License)
def UpdateLicenseEndDate(sender, instance, **kwargs):
    UpdateEndDate(instance)


@receiver(pre_save, sender=Conseil)
def UpdateConseilEndDate(sender, instance, **kwargs):
    UpdateEndDate(instance)


@receiver([post_save, post_delete], sender=License)
def LicenseUpdateContractPrice(sender, instance, **kwargs):
    UpdateContractPrice(instance.contract)


@receiver([post_save, post_delete], sender=Conseil)
def ConseilUpdateContractPrice(sender, instance, **kwargs):
    UpdateContractPrice(instance.contract)


@receiver(post_save, sender=Invite)
def SendInvite(sender, instance, **kwargs):
    subject = 'Invitation à rejoindre Easley'
    message = "Une personne vous à invité à rejoindre son entreprise sur Easley.\n\n\
Veuillez vous rendre sur cette page pour créer votre compte\n\n\
https://easleymvp.herokuapp.com%s\n\n\
Merci d'utiliser notre site !\n\n\
L'équipe d'Easley\n" % reverse('mvp-join-company', args=[instance.email])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [instance.email, ]
    send_mail(subject, message, email_from, recipient_list)
