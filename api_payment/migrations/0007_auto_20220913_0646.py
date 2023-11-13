# Generated by Django 3.2.4 on 2022-09-13 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0006_auto_20220805_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenttransfer',
            name='time_remaining',
        ),
        migrations.AddField(
            model_name='paymenttransfer',
            name='expired',
            field=models.DateTimeField(blank=True, db_column='expired', null=True, verbose_name='expired'),
        ),
    ]
