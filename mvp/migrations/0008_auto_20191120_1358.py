# Generated by Django 2.2.7 on 2019-11-20 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0007_auto_20191120_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Factu Manager'), (2, 'Account Manager'), (1, 'Manager')], default=None, verbose_name="manager's type"),
        ),
    ]