from django.db.models.signals import post_delete, post_save, pre_save
from django.db.models import Sum
from django.dispatch import receiver
from .models import Company, Commercial, Manager, Client, Conseil, License, Contract
from dateutil.relativedelta import relativedelta


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
