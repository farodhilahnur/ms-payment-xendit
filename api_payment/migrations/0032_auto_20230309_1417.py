# Generated by Django 3.2.4 on 2023-03-09 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0031_auto_20230309_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='expired_date_date',
        ),
        migrations.AddField(
            model_name='invoice',
            name='expired_date',
            field=models.DateTimeField(blank=True, db_column='expired_date', null=True, verbose_name='Expiration Date'),
        ),
    ]
