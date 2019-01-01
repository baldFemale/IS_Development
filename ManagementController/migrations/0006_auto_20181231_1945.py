# Generated by Django 2.1.4 on 2018-12-31 11:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ManagementController', '0005_auto_20181226_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='OccupationTime',
            field=models.PositiveSmallIntegerField(choices=[(0, '中饭'), (1, '晚饭')]),
        ),
        migrations.AlterField(
            model_name='table',
            name='OpenTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 31, 11, 45, 20, 747901, tzinfo=utc)),
        ),
    ]
