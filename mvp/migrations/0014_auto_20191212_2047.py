# Generated by Django 2.2.7 on 2019-12-12 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0013_auto_20191212_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager General'), (2, 'Account Manager'), (3, 'Factu Manager')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
    ]
