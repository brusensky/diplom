# Generated by Django 2.1.7 on 2019-06-12 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='type_of_delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Название')),
                ('formule', models.CharField(max_length=100, verbose_name='Формула')),
                ('variableY', models.IntegerField(verbose_name='Значение переменной Y')),
            ],
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 12, 22, 9, 51, 400392)),
        ),
    ]
