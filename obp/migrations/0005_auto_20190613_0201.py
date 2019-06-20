# Generated by Django 2.1.7 on 2019-06-12 23:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0004_auto_20190613_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type_of_delivery',
            name='formule',
        ),
        migrations.RemoveField(
            model_name='type_of_delivery',
            name='variableX1',
        ),
        migrations.RemoveField(
            model_name='type_of_delivery',
            name='variableX2',
        ),
        migrations.AddField(
            model_name='type_of_delivery',
            name='formule1',
            field=models.CharField(default='x', max_length=100, verbose_name='Формула если сумма заказа < Y'),
        ),
        migrations.AddField(
            model_name='type_of_delivery',
            name='formule2',
            field=models.CharField(default='x', max_length=100, verbose_name='Формула если сумма заказа > Y'),
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 13, 2, 11, 10, 658242)),
        ),
    ]
