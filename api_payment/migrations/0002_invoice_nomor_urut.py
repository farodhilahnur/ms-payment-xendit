# Generated by Django 3.2.4 on 2022-08-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='nomor_urut',
            field=models.IntegerField(blank=True, db_column='nomor_urut', null=True, verbose_name='Nomor urut'),
        ),
    ]
