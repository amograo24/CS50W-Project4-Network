# Generated by Django 3.2.4 on 2021-08-09 03:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 9, 9, 23, 8, 466006)),
        ),
    ]
