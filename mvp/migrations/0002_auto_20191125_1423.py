# Generated by Django 2.2.7 on 2019-11-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Account'), (1, 'Manager'), (3, 'Factu')], default=None, verbose_name="manager's type"),
        ),
    ]