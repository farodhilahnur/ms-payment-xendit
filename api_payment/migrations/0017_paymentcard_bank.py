# Generated by Django 3.2.4 on 2022-10-09 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0016_auto_20221009_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='bank',
            field=models.CharField(blank=True, db_column='bank', max_length=1000, null=True, verbose_name='Bank'),
        ),
    ]
