# Generated by Django 2.2.7 on 2019-11-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0034_auto_20191106_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'CEO'), (1, 'DEV'), (4, 'Commercial'), (2, 'STAFF')], default=4, verbose_name='user type'),
        ),
    ]