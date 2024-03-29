# Generated by Django 2.1.7 on 2019-06-19 20:33

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obp', '0016_auto_20190619_2320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='special_offers',
            options={'verbose_name': 'Специальное предложение', 'verbose_name_plural': 'Специальные предложения'},
        ),
        migrations.AddField(
            model_name='special_offers',
            name='title',
            field=models.CharField(max_length=30, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='client_auth',
            name='end_of_live',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 19, 23, 43, 43, 651405)),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='вес'),
        ),
    ]
