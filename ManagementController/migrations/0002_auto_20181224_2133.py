# Generated by Django 2.1.3 on 2018-12-24 13:33

import ManagementController.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManagementController', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to=ManagementController.models.get_file_path),
        ),
    ]
