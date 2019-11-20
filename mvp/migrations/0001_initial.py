# Generated by Django 2.2.7 on 2019-11-17 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, help_text="Indicated client's name", max_length=150, verbose_name="client's name")),
                ('email', models.EmailField(default=None, help_text="Indicate client's email", max_length=150, verbose_name="client's email")),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'ordering': ['company', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Commercial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Commercial',
                'verbose_name_plural': 'Commercials',
                'ordering': ['company__id', 'user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="company's name", max_length=150, verbose_name="company's name")),
                ('ceo', models.OneToOneField(help_text="Indicate company's manager", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="company's manager")),
            ],
            options={
                'verbose_name': 'entreprise',
                'verbose_name_plural': 'entreprises',
                'ordering': ['ceo__id'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300, verbose_name="service's description")),
                ('pricing', models.PositiveIntegerField(default=0, help_text='pricing du service (EN EUROS)', verbose_name='pricing du service')),
                ('estimated_date', models.DateTimeField(default=django.utils.timezone.now, help_text='date prévisionelle ???(en mois/jours).', verbose_name='date prévisionelle ???')),
                ('actual_date', models.DateTimeField(default=django.utils.timezone.now, help_text='fin du Service (ACTUEL)(en mois/jours).', verbose_name='fin du Service (ACTUEL ???)')),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Client', verbose_name="service's client")),
                ('commercial', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Commercial', verbose_name="service's commercial")),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Company', verbose_name="service's company")),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'ordering': ['pricing', 'company__id', 'description'],
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'manager',
                'verbose_name_plural': 'managers',
                'ordering': ['company__id'],
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='description de la license', max_length=300, verbose_name="license's description")),
                ('cost', models.PositiveIntegerField(default=0, help_text='coût de la license (EN EUROS)', verbose_name='coût de la license')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, help_text='date de début (en mois/jours).', verbose_name='date de début')),
                ('duration', models.DurationField(default='21 days', help_text='durée de la license (en mois/jours).', verbose_name='durée de la license')),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Client', verbose_name="license's client")),
                ('commercial', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Commercial', verbose_name="license's commercial")),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mvp.Company', verbose_name="license's company")),
            ],
            options={
                'verbose_name': 'license',
                'verbose_name_plural': 'licenses',
                'ordering': ['cost', 'company__id', 'description'],
            },
        ),
        migrations.AddField(
            model_name='commercial',
            name='company',
            field=models.ForeignKey(default=None, help_text='Indicate Company ID', on_delete=django.db.models.deletion.CASCADE, to='mvp.Company'),
        ),
        migrations.AddField(
            model_name='commercial',
            name='user',
            field=models.OneToOneField(default=None, help_text='Indicate User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='commercial',
            field=models.ForeignKey(default=None, help_text="Indicate client's commercial", on_delete=django.db.models.deletion.CASCADE, to='mvp.Commercial', verbose_name="client's commercial"),
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(default=None, help_text="Indicate client's company", on_delete=django.db.models.deletion.CASCADE, to='mvp.Company', verbose_name="client's company"),
        ),
    ]