# Generated by Django 2.2.7 on 2019-11-24 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0030_auto_20191124_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (3, 'Factu'), (2, 'Account')], default=None, verbose_name="manager's type"),
        ),
    ]
