# Generated by Django 2.1.7 on 2019-06-19 20:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0018_auto_20190619_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 19, 23, 44, 50, 180766)),
        ),
    ]
