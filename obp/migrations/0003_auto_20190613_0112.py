# Generated by Django 2.1.7 on 2019-06-12 22:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0002_auto_20190612_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=100, null=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 13, 1, 22, 1, 529981)),
        ),
    ]