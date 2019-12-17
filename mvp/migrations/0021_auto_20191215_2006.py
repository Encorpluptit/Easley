# Generated by Django 2.2.7 on 2019-12-15 20:06

from django.db import migrations, models
import django.db.models.deletion
import mvp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0020_auto_20191215_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conseil',
            name='description',
            field=models.CharField(help_text='description du conseil', max_length=150, verbose_name="conseil's description"),
        ),
        migrations.AlterField(
            model_name='conseil',
            name='duration',
            field=models.PositiveIntegerField(default=1, help_text='précisez la durée totale du conseil (en mois).', verbose_name='durée totale du conseil (en mois).'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='duration',
            field=models.PositiveIntegerField(default=1, help_text='précisez la durée totale du contrat (en mois).', verbose_name='durée totale du contrat (en mois).'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (3, 'Responsable Facturation'), (4, 'Commercial'), (2, 'Responsable Clientèle')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='license',
            name='contract',
            field=models.ForeignKey(default=None, help_text='préciser le contrat dans lequel est inclus cette licence.', on_delete=django.db.models.deletion.CASCADE, to='mvp.Contract', verbose_name='le contrat dans lequel est inclus cette licence.'),
        ),
        migrations.AlterField(
            model_name='license',
            name='duration',
            field=models.PositiveIntegerField(default=1, help_text='précisez la durée totale de la licence (en mois).', verbose_name='durée totale de la licence.'),
        ),
        migrations.AlterField(
            model_name='license',
            name='end_date',
            field=models.DateField(default=mvp.models.GetDate, help_text='date de fin de la licence.', verbose_name='date de fin de la licence.'),
        ),
        migrations.AlterField(
            model_name='license',
            name='payed',
            field=models.BooleanField(default=False, help_text='précisez si la licence est déjà payée.', verbose_name='si la licence est payée.'),
        ),
        migrations.AlterField(
            model_name='license',
            name='price',
            field=models.PositiveIntegerField(default=0, help_text='coût de la licence (€).', verbose_name='coût de la licence'),
        ),
        migrations.AlterField(
            model_name='license',
            name='start_date',
            field=models.DateField(default=mvp.models.GetDate, help_text='date de début de la licence.', verbose_name='date de début de la licence.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(1, 'Effectué'), (0, 'Pas encore effectué'), (2, 'Ne sera jamais effectué')], default=0, help_text='précisez si le service est effectué.', verbose_name='si le service est effectué.'),
        ),
    ]