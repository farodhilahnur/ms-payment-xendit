# Generated by Django 3.2.4 on 2022-10-09 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0017_paymentcard_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentcard',
            name='redicret_url',
        ),
        migrations.AddField(
            model_name='paymentcard',
            name='redirect_url',
            field=models.CharField(blank=True, db_column='redirect_url', max_length=1000, null=True, verbose_name='redirect url'),
        ),
    ]
