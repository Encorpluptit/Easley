from django.db.models.signals import post_delete, post_save
from django.db.models import Sum
from django.dispatch import receiver
from .models import Company, Commercial, Manager, Client, Conseil, License


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


@receiver([post_save, post_delete], sender=License)
def LicenseUpdateContractPrice(sender, instance, **kwargs):
    UpdateContractPrice(instance.contract)


@receiver([post_save, post_delete], sender=Conseil)
def ConseilUpdateContractPrice(sender, instance, **kwargs):
    UpdateContractPrice(instance.contract)