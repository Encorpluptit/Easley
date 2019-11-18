from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Company(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="company's name",
        help_text="company's name",
    )
    ceo = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="company's manager",
        help_text="Indicate company's manager",
    )

    class Meta:
        verbose_name = "entreprise"
        verbose_name_plural = "entreprises"
        ordering = ['ceo__id']

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "manager"
        verbose_name_plural = "managers"
        ordering = ['company__id']

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Commercial(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        on_delete=models.CASCADE,
        help_text="Indicate User",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        help_text="Indicate Company ID"
    )

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commercials"
        ordering = ['company__id', 'user__first_name', 'user__last_name']

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Client(models.Model):
    name = models.CharField(
        max_length=150,
        default=None,
        verbose_name="client's name",
        help_text="Indicated client's name"
    )
    email = models.EmailField(
        max_length=150,
        default=None,
        verbose_name="client's email",
        help_text="Indicate client's email",
    )
    commercial = models.ForeignKey(
        Commercial,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="client's commercial",
        help_text="Indicate client's commercial",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="client's company",
        help_text="Indicate client's company",
    )

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"
        ordering = ['company', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self, comp_id):
        print(reverse('mvp-client-details', args=[comp_id, str(self.id)]))
        return reverse('mvp-client-details', args=[comp_id, str(self.id)])


class Service(models.Model):
    description = models.CharField(
        max_length=300,
        verbose_name="service's description",
    )
    client = models.ForeignKey(
        Client,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="service's client",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="service's company",
    )
    commercial = models.ForeignKey(
        Commercial,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="service's commercial",
    )
    pricing = models.PositiveIntegerField(
        default=0,
        verbose_name="pricing du service",
        help_text="pricing du service (EN EUROS)"
    )
    # invoice
    estimated_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="date prévisionelle ???",
        help_text="date prévisionelle ???(en mois/jours)."
    )
    actual_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="fin du Service (ACTUEL ???)",
        help_text="fin du Service (ACTUEL)(en mois/jours)."
    )

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ['pricing', 'company__id', 'description']

    def __str__(self):
        return self.description


class License(models.Model):
    description = models.CharField(
        max_length=300,
        # name="subject",
        verbose_name="license's description",
        help_text="description de la license"
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="license's company",
        # related_name="company's licenses+",
        # related_query_name="company's licenses",
    )
    commercial = models.ForeignKey(
        Commercial,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="license's commercial",
    )
    client = models.ForeignKey(
        Client,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="license's client",
    )
    cost = models.PositiveIntegerField(
        default=0,
        verbose_name="coût de la license",
        help_text="coût de la license (EN EUROS)"
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="date de début",
        help_text="date de début (en mois/jours)."
    )
    duration = models.DurationField(
        default='21 days',
        verbose_name="durée de la license",
        help_text="durée de la license (en mois/jours)."
    )

    class Meta:
        verbose_name = "license"
        verbose_name_plural = "licenses"
        ordering = ['cost', 'company__id', 'description']

    def __str__(self):
        return self.description


# @TODO: Invoice model
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
# - commercial(le
# commercial)
# manytomany Service
# manytomany or OneToOne or Foreignkey(peut être pas ici la foreign key)
# contract_type
# contract_





# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, default=None, on_delete=models.CASCADE)
#     type = models.PositiveSmallIntegerField(
#         verbose_name="user's type",
#         default=4,
#         choices={
#             (1, 'DEV'),
#             (2, 'STAFF'),
#             (3, 'CEO'),
#             (4, 'Commercial')
#         },
#     )
#     # company2 = models.ManyToOneRel()
#     company = models.ForeignKey(
#         Companies,
#         default=None,
#         on_delete=models.CASCADE,
#         null=True
#     )
#
#     class Meta:
#         verbose_name = "profile"
#         verbose_name_plural = "profiles"
#         ordering = ['user_id']
#
#     def __str__(self):
#         if self.user.first_name:
#             return self.user.first_name
#         else:
#             return self.user.username

# from django.dispatch import receiver
# from django.db.models.signals import post_save
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#
