# Generated by Django 3.2.4 on 2023-03-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0029_paymenttransfermanual_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='sub_total',
            field=models.BigIntegerField(blank=True, db_column='sub_total', null=True, verbose_name='Sub total'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.BigIntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price_user',
            field=models.BigIntegerField(blank=True, db_column='total_price_user', null=True, verbose_name='Total Price User'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total_amount',
            field=models.BigIntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='paymentcard',
            name='total_amount',
            field=models.BigIntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='paymenttransfer',
            name='total_amount',
            field=models.BigIntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='paymenttransfermanual',
            name='total_amount',
            field=models.BigIntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
    ]
