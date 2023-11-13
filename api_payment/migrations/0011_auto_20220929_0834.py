# Generated by Django 3.2.4 on 2022-09-29 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0010_alter_invoice_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='expired',
            field=models.DateTimeField(blank=True, db_column='expired', null=True, verbose_name='expired'),
        ),
        migrations.AddField(
            model_name='paymentcard',
            name='transaction_time',
            field=models.DateTimeField(blank=True, db_column='transaction_time', null=True, verbose_name='transaction time'),
        ),
        migrations.AddField(
            model_name='paymenttransfer',
            name='transaction_time',
            field=models.DateTimeField(blank=True, db_column='transaction_time', null=True, verbose_name='transaction time'),
        ),
    ]