# Generated by Django 2.2.7 on 2019-11-06 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0038_auto_20191106_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(2, 'STAFF'), (4, 'Commercial'), (3, 'CEO'), (1, 'DEV')], default=4, verbose_name='user type'),
        ),
    ]