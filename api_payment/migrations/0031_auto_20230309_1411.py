# Generated by Django 3.2.4 on 2023-03-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0030_auto_20230309_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='expired_date',
        ),
        migrations.RemoveField(
            model_name='paymentcard',
            name='expired',
        ),
        migrations.RemoveField(
            model_name='paymenttransfer',
            name='expired',
        ),
        migrations.RemoveField(
            model_name='paymenttransfermanual',
            name='expired',
        ),
        migrations.AddField(
            model_name='invoice',
            name='expired_date_date',
            field=models.DateTimeField(blank=True, db_column='expired_date_date', null=True, verbose_name='Expiration Date'),
        ),
        migrations.AddField(
            model_name='paymentcard',
            name='expired_date',
            field=models.DateTimeField(blank=True, db_column='expired_date', null=True, verbose_name='expired_date'),
        ),
        migrations.AddField(
            model_name='paymenttransfer',
            name='expired_date',
            field=models.DateTimeField(blank=True, db_column='expired_date', null=True, verbose_name='expired_date'),
        ),
        migrations.AddField(
            model_name='paymenttransfermanual',
            name='expired_date',
            field=models.DateTimeField(blank=True, db_column='expired_date', null=True, verbose_name='expired_date'),
        ),
    ]
