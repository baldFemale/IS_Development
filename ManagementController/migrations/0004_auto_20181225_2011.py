# Generated by Django 2.1.4 on 2018-12-25 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManagementController', '0003_auto_20181224_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='CloseTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='OpenTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
