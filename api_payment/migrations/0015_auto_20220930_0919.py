# Generated by Django 3.2.4 on 2022-09-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_payment', '0014_auto_20220930_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(blank=True, db_column='status', default='hold', max_length=1000, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.IntegerField(blank=True, db_column='tax', null=True, verbose_name='Tax'),
        ),
    ]
