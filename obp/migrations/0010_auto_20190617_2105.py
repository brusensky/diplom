# Generated by Django 2.1.7 on 2019-06-17 18:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0009_auto_20190614_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliveryCost',
            field=models.IntegerField(null=True, verbose_name='сумма доставки'),
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 17, 21, 15, 47, 71953)),
        ),
        migrations.AlterField(
            model_name='order',
            name='apartament_number',
            field=models.PositiveIntegerField(null=True, verbose_name='квартира'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=25, null=True, verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='order',
            name='entrance',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='этаж'),
        ),
        migrations.AlterField(
            model_name='order',
            name='house',
            field=models.PositiveIntegerField(null=True, verbose_name='номер дома'),
        ),
        migrations.AlterField(
            model_name='order',
            name='street',
            field=models.CharField(max_length=25, null=True, verbose_name='улица'),
        ),
    ]