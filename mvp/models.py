from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Create your models here.


class Company(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="nom de l'entreprise.",
        help_text="préciser le nom de l'entreprise.",
    )
    ceo = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="CEO de l'entreprise.",
        help_text="préciser le CEO de l'entreprise.",
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
        verbose_name="l'utilisateur lié à ce manager",
        help_text="préciser l'utilisateur lié à ce manager.",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="entreprise du manager.",
        help_text="préciser l'entreprise de ce manager.",
    )
    role = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="rôle du manager.",
        help_text="préciser son rôle.",
        choices={
            (1, 'Manager General'),
            (2, 'Account Manager'),
            (3, 'Factu Manager'),
        },
    )

    class Meta:
        verbose_name = "manager"
        verbose_name_plural = "managers"
        ordering = ['company__id', 'role', 'user', 'user__first_name', 'user__last_name']

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Commercial(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="l'utilisateur lié à ce commercial.",
        help_text="préciser l'utilisateur lié à ce commercial.",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="l'entreprise de ce commercial.",
        help_text="préciser l'entreprise de ce commercial."
    )

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commercials"
        ordering = ['company__id', 'user', 'user__first_name', 'user__last_name']

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Client(models.Model):
    name = models.CharField(
        max_length=150,
        default=None,
        verbose_name="le nom du client.",
        help_text="le nom du client."
    )
    email = models.EmailField(
        max_length=150,
        default=None,
        verbose_name="email du client",
        help_text="l'email du client",
    )
    commercial = models.ForeignKey(
        Commercial,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le commercial ayant ramené le client.",
        help_text="préciser le commercial relatif à ce client.",
    )
    account_manager = models.ForeignKey(
        Manager,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le responsable clientièle de ce client.",
        help_text="préciserle responsable clientièle de ce client.",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="l'entreprise du client.",
        help_text="préciser l'entreprise du client.",
    )

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "client"
        ordering = ['company__id', 'commercial__id', 'account_manager__id', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self, comp_id):
        return reverse('mvp-client-details', args=[comp_id, str(self.id)])


class Contract(models.Model):
    description = models.CharField(
        max_length=100,
        verbose_name="description du contrat",
        help_text="description du contrat",
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="date de début du contrat",
        help_text="date de début du contrat"
    )
    end_date = models.DateField(
        default=timezone.now() + relativedelta(months=1),
        verbose_name="date de fin du contrat",
        help_text="date de fin du contrat."
    )
    facturation = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Fréquance de la facturation.",
        help_text="Fréquence de la facturation.",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="montant total du contrat.",
        help_text="montant total du contrat (EN EUROS)",
    )
    payed = models.BooleanField(
        default=False,
        verbose_name="si le contrat est payé en intégralité.",
        help_text="précisez si le contrat est payé en intégralité.",
    )
    client = models.ForeignKey(
        Client,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="client cible du contrat",
        help_text="client cible du contrat",
    )
    company = models.ForeignKey(
        Company,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="entreprise vendeuse du contrat.",
        help_text="entreprise vendeuse du contrat.",
    )
    commercial = models.ForeignKey(
        Commercial,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="commercial à l'origine du contrat",
        help_text="commercial à l'origine du contrat",
    )
    factu_manager = models.ForeignKey(
        Manager,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le responsable de la facturation de ce contrat.",
        help_text="préciserle responsable de la facturation de ce contrat.",
        related_name="factu_manager"
    )
    validated = models.BooleanField(
        default=False,
        verbose_name="si le contract est validé.",
        help_text="précisez si le contract est validé..",
    )

    class Meta:
        verbose_name = "conseil"
        verbose_name_plural = "conseils"
        ordering = ['company__id', 'commercial__id', 'price', 'description']

    def __str__(self):
        return self.description

    def get_absolute_url(self, comp_id):
        return reverse('mvp-contract-details', args=[comp_id, str(self.id)])


class Invoice(models.Model):
    description = models.CharField(
        max_length=300,
        verbose_name="invoice's description",
        help_text="description de la facture",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="montant total de la facture.",
        help_text="montant total de la facture (EN EUROS).",
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="date de la facture",
        help_text="date de la facture."
    )
    payed = models.BooleanField(
        default=False,
        verbose_name="si la facture est payée.",
        help_text="précisez si la facture est payée",
    )
    contract = models.ForeignKey(
        Contract,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le ou les conseil(s) relatif(s) à cette facture.",
        help_text="préciser le ou les conseil(s) à facturer.",
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="l'entreprise de cette facture.",
        help_text="préciser l'entreprise de cette facture.",
    )

    class Meta:
        verbose_name = "facture"
        verbose_name_plural = "factures"
        ordering = ['company__id', 'payed', 'price', 'description']

    def __str__(self):
        return self.description

    def get_absolute_url(self, comp_id):
        return reverse('mvp-invoice-details', args=[comp_id, str(self.id)])


class Conseil(models.Model):
    description = models.TextField(
        max_length=300,
        verbose_name="conseil's description",
        help_text="description du conseil",
    )
    contract = models.ForeignKey(
        Contract,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le contrat dans lequel est inclus ce conseil.",
        help_text="préciser le contrat dans lequel est inclus ce conseil.",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="montant total du conseil.",
        help_text="montant total du conseil (EN EUROS)",
    )
    payed = models.BooleanField(
        default=False,
        verbose_name="si le conseil est payé.",
        help_text="précisez si le conseil est déjà payé.",
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="date de début du conseil",
        help_text="date de début du conseil"
    )
    end_date = models.DateField(
        default=timezone.now() + relativedelta(months=1),
        verbose_name="date de fin du conseil",
        help_text="date de fin du conseil."
    )
    invoice = models.ForeignKey(
        Invoice,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="la facture relative à ce conseil",
        help_text="la facture relative à ce conseil.",
    )
    # company = models.ForeignKey(
    #     Company,
    #     default=None,
    #     on_delete=models.CASCADE,
    #     verbose_name="entreprise de ce conseil",
    #     help_text="entreprise de ce conseil",
    # )
    # client = models.ForeignKey(
    #     Client,
    #     default=None,
    #     on_delete=models.CASCADE,
    #     verbose_name="client cible du contrat",
    #     help_text="client cible du contrat",
    # )

    class Meta:
        verbose_name = "conseil"
        verbose_name_plural = "conseils"
        ordering = ['contract__id', 'payed', 'price', 'description']

    def __str__(self):
        return self.description

    def get_absolute_url(self, comp_id, contract_id):
        return reverse('mvp-conseil-details', args=[comp_id, contract_id, str(self.id)])


class Service(models.Model):
    description = models.CharField(
        max_length=150,
        verbose_name="description du service",
        help_text="description du service",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="pricing du service",
        help_text="pricing du service (EN EUROS)",
    )
    conseil = models.ForeignKey(
        Conseil,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="conseil relatif au service",
        help_text="conseil relatif au service",
    )
    estimated_date = models.DateField(
        default=timezone.now,
        verbose_name="date prévisionelle ???",
        help_text="date prévisionelle ???(en mois/jours)."
    )
    actual_date = models.DateField(
        default=timezone.now,
        verbose_name="fin du service (ACTUEL ???)",
        help_text="fin du service (ACTUEL)(en mois/jours)."
    )
    payed = models.BooleanField(
        default=False,
        verbose_name="si le service est payé.",
        help_text="précisez si le service est déjà payé.",
    )

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ['payed', 'estimated_date', 'price']


class License(models.Model):
    description = models.CharField(
        max_length=150,
        verbose_name="description de la license.",
        help_text="description de la license"
    )
    contract = models.ForeignKey(
        Contract,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="le contrat dans lequel est inclus ce conseil.",
        help_text="préciser le contrat dans lequel est inclus ce conseil.",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="coût de la license",
        help_text="coût de la license (EN EUROS)"
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="date de début",
        help_text="date de début (en mois/jours)."
    )
    end_date = models.DateField(
        default=timezone.now() + relativedelta(months=1),
        verbose_name="durée de la license",
        help_text="durée de la license (en mois/jours)."
    )
    payed = models.BooleanField(
        default=False,
        verbose_name="si la license est payée.",
        help_text="précisez si la license est déjà payée.",
    )
    invoice = models.ForeignKey(
        Invoice,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="la facture relative à cette license",
        help_text="la facture relative à cette license.",
    )
    # company = models.ForeignKey(
    #     Company,
    #     default=None,
    #     on_delete=models.CASCADE,
    #     verbose_name="entreprise de cette license",
    #     help_text="entreprise de cette license",
    # )
    # client = models.ForeignKey(
    #     Client,
    #     default=None,
    #     on_delete=models.CASCADE,
    #     verbose_name="license's client",
    #     help_text="précisez le client achetant cette license.."
    # )

    class Meta:
        verbose_name = "license"
        verbose_name_plural = "licenses"
        ordering = ['contract__id', 'price', 'description']

    def __str__(self):
        return self.description

    def get_absolute_url(self, comp_id, contract_id):
        return reverse('mvp-license-details', args=[comp_id, contract_id, str(self.id)])

# - invoices
# - company_id
# - client_id
# - commercial(le
# commercial)
# manytomany Conseil
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
