# Generated by Django 3.2.4 on 2022-09-29 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0009_auto_20220914_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_date',
            field=models.DateTimeField(blank=True, db_column='payment_date', null=True, verbose_name='Payment Date'),
        ),
    ]