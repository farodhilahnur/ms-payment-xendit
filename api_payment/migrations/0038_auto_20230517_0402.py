# Generated by Django 3.2.4 on 2023-05-17 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0037_auto_20230504_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='plan',
            field=models.CharField(blank=True, db_column='plan', max_length=1000, null=True, verbose_name='plan'),
        ),
        migrations.AddField(
            model_name='setting',
            name='plan',
            field=models.CharField(blank=True, db_column='plan', max_length=1000, null=True, verbose_name='plan'),
        ),
    ]
