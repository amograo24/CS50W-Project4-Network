# Generated by Django 3.2.4 on 2021-08-13 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20210810_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 13, 13, 51, 17, 977335)),
        ),
    ]
