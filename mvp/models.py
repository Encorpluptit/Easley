from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, default=None, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(
        verbose_name="user type",
        name="type",
        default=4,
        choices={
            (1, 'DEV'),
            (2, 'STAFF'),
            (3, 'CEO'),
            (4, 'Commercial')
        },
    )

    class Meta:
        verbose_name = "profile"
        # verbose_name_plural
        ordering = ['user_id']

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Companies(models.Model):
    name = models.CharField("company name", max_length=70)
    ceo = models.OneToOneField(
        User,
        default=None,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name="company's ceo"
    )

    class Meta:
        verbose_name = "entreprise"
        # verbose_name_plural
        ordering = ['name']

    def __str__(self):
        return self.name


class Clients(models.Model):
    name = models.CharField("client name", default="client", max_length=50)
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name="clients",
        related_query_name="clients",
    )

    class Meta:
        verbose_name = "client"
        # verbose_name_plural
        ordering = ['company']

    def __str__(self):
        return self.name


class License(models.Model):
    subject = models.CharField(
        "",
        name="subject",
        max_length=300,
        # verbose_name="subject",
        help_text="sujet de la license"
    )
    company = models.ForeignKey(
        Companies,
        default=None,
        on_delete=models.CASCADE,
        related_name="company's licenses+",
        related_query_name="company's licenses",
    )
    cost = models.PositiveIntegerField(
        default=0,
        verbose_name="coût de la license",
        help_text="coût de la license (EN EUROS)"
    )
    start = models.DateTimeField(
        default=timezone.now,
        verbose_name="date de début",
        help_text="date de début (en mois/jours)."
    )
    duration = models.DurationField(
        verbose_name="durée de la license",
        help_text="durée de la license (en mois/jours)."
    )

    class Meta:
        verbose_name = "License"
        # verbose_name_plural
        ordering = ['cost']

    def __str__(self):
        return self.subject


class Service(models.Model):
    description = models.CharField("description", max_length=300)
    company = models.ForeignKey(
        Companies,
        default=None,
        on_delete=models.CASCADE,
        related_name="company's services+",
        related_query_name="company's services",
    )
    pricing = models.PositiveIntegerField(
        default=0,
        verbose_name="pricing du service",
        help_text="pricing du service (EN EUROS)"
    )
    # invoice
    estimated_date = models.DateTimeField(
        verbose_name="date prévisionelle ???",
        help_text="date prévisionelle ???(en mois/jours)."
    )
    actual_date = models.DateTimeField(
        verbose_name="fin du Service (ACTUEL ???)",
        help_text="fin du Service (ACTUEL)(en mois/jours)."
    )

    class Meta:
        verbose_name = "service"
        # verbose_name_plural
        ordering = ['pricing']

    def __str__(self):
        return self.description

#
#
# class Invoice(models.Model):
#     company = models.ForeignKey(
#         Companies,
#         on_delete=models.CASCADE,
#         related_name="company's invoices+",
#         related_query_name="company's invoices",
#     )
#     client = models.ForeignKey(
#         Clients,
#         on_delete=models.CASCADE,
#         related_name="invoice's client+",
#         related_query_name="invoice's client",
#     )
#     commercial = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="commercial",
#         related_query_name="client's commercial",
#     )

# - invoices
# - company_id
# - client_id
# - user_id(le
# commercial)
