# Generated by Django 3.2.4 on 2022-08-05 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0003_auto_20220805_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttransfer',
            name='virtual_account',
            field=models.BigIntegerField(blank=True, db_column='virtual_account', null=True, verbose_name='Virtual Account'),
        ),
    ]