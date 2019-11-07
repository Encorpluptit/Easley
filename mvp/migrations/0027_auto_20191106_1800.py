# Generated by Django 2.2.7 on 2019-11-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0026_auto_20191106_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(4, 'Commercial'), (1, 'DEV'), (2, 'STAFF'), (3, 'CEO')], default=4, unique=True, verbose_name='user type'),
        ),
    ]