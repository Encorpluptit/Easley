# Generated by Django 2.2.7 on 2019-11-23 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0024_auto_20191123_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Factu'), (1, 'Manager'), (2, 'Account')], default=None, verbose_name="manager's type"),
        ),
    ]