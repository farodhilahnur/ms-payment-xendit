# Generated by Django 3.2.4 on 2022-09-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0012_auto_20220930_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='sub_total',
            field=models.IntegerField(blank=True, db_column='sub_total', null=True, verbose_name='Sub total'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.IntegerField(blank=True, db_column='tax', null=True, verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.IntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price_user',
            field=models.IntegerField(blank=True, db_column='total_price_user', null=True, verbose_name='Total Price User'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total_amount',
            field=models.IntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='paymentcard',
            name='total_amount',
            field=models.IntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='paymenttransfer',
            name='total_amount',
            field=models.IntegerField(blank=True, db_column='total_amount', null=True, verbose_name='Total amount'),
        ),
    ]
