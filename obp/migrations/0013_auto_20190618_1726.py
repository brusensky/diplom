# Generated by Django 2.1.7 on 2019-06-18 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0012_auto_20190617_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='номер телефона'),
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 18, 17, 36, 11, 572093)),
        ),
    ]
