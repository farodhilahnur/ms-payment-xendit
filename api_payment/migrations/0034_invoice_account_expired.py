# Generated by Django 3.2.4 on 2023-03-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0033_auto_20230316_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='account_expired',
            field=models.DateTimeField(blank=True, db_column='account_expired', null=True, verbose_name='Expiration account'),
        ),
    ]
