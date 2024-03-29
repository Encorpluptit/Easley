# Generated by Django 2.2.7 on 2020-02-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0011_auto_20200119_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='facturation_delay',
            field=models.PositiveSmallIntegerField(choices=[(15, '15 Jours'), (45, '45 Jours'), (60, '60 Jours'), (90, '90 Jours'), (30, '30 Jours'), (75, '75 Jours')], default=45, help_text='Précisez le délai à partir duquel un client est considéré en retard de paiement.', verbose_name='Délai de facturation.'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (4, 'Commercial'), (3, 'Responsable Facturation'), (2, 'Responsable Clientèle')], default=4, help_text='Préciser le rôle de la personne', verbose_name='Rôle de la personne'),
        ),
    ]
