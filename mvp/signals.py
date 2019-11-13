from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Company, Ceo


@receiver(post_delete, sender=Company)
def auto_delete_ceo_with_company(sender, instance, **kwargs):
    instance.ceo.delete()