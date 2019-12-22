from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Conseil, License, Contract, Invite


def UpdateContractPrice(contract):
    contract.price = 0
    licenses_price = contract.license_set.aggregate(Sum('price'))
    contract.price += licenses_price['price__sum'] or 0
    conseils_price = contract.conseil_set.aggregate(Sum('price'))
    contract.price += conseils_price['price__sum'] or 0
    contract.save()


def UpdateEndDate(instance):
    instance.end_date = instance.start_date + relativedelta(months=+instance.duration)


def SmallTryExcept(num, denom):
    try:
        return Decimal(num / denom)
    except:
        return 0


def UpdateServicesPrices(services, instance):
    context = services.aggregate(senior=Sum('senior_day'), junior=Sum('junior_day'))
    seniority_ratio = SmallTryExcept(instance.contract.company.senior_day, instance.contract.company.junior_day)
    # print(context, type(context))
    total_junior_time, total_senior_time = context['junior'], context['senior']
    total_time = total_junior_time + total_senior_time
    # print("seniority ratio:\t", seniority_ratio)
    # print("total_price:\t", instance.price)
    # print("TOTAL_time:\t", total_time)
    # print("total_JUNIOR_time:\t", total_junior_time)
    # print("total_SENIOR_time:\t", total_senior_time)
    temp = total_senior_time * Decimal(seniority_ratio)
    # total_time_senior_ratio = temp / (temp + total_junior_time)
    total_time_senior_ratio = SmallTryExcept(temp, temp + total_junior_time)
    total_time_junior_ratio = 1 - total_time_senior_ratio
    # print("total senior time :\t%.3f" % total_time_senior_ratio)
    # print("total junior time:\t", total_time_junior_ratio)
    # total_price_senior = instance.price * total_time_senior_ratio
    # total_price_junior = instance.price * total_time_junior_ratio
    # print("total senior price :\t%.3f" % total_price_senior)
    # print("total junior price:\t", total_price_junior)
    unity_price_senior = SmallTryExcept(instance.price * total_time_senior_ratio, total_senior_time)
    unity_price_junior = SmallTryExcept(instance.price * total_time_junior_ratio, total_junior_time)
    # unity_price_senior = (instance.price * total_time_senior_ratio) / total_senior_time
    # unity_price_junior = (instance.price * total_time_junior_ratio) / total_junior_time
    # print("unity senior price :\t%.3f" % unity_price_senior)
    # print("unity junior price:\t%d" % unity_price_junior)
    for service in services:
        junior_cost = service.junior_day * unity_price_junior
        # print(junior_cost)
        senior_cost = service.senior_day * unity_price_senior
        # print(senior_cost)
        service.price = int(junior_cost + senior_cost)
        service.save()


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


@receiver(post_delete, sender=Conseil)
def ConseilDeleteContractPrice(sender, instance, **kwargs):
    UpdateContractPrice(instance.contract)


@receiver(post_save, sender=Conseil)
def ConseilUpdate(sender, instance, update_fields=None, **kwargs):
    UpdateContractPrice(instance.contract)
    if not update_fields or 'price' not in update_fields:
        return
    services = instance.service_set.all() or None
    if services:
        UpdateServicesPrices(services, instance)


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
