# Generated by Django 2.1.7 on 2019-06-14 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0008_auto_20190613_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 14, 21, 48, 44, 179056)),
        ),
    ]
