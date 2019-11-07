# Generated by Django 2.2.7 on 2019-11-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0022_auto_20191106_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(2, 'STAFF'), (3, 'CEO'), (4, 'Commercial'), (1, 'DEV')], default=4, unique=True, verbose_name='user type'),
        ),
    ]