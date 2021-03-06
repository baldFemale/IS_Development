# Generated by Django 2.1.4 on 2018-12-23 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ApplyController', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Result', models.PositiveIntegerField(choices=[(0, '通过'), (1, '拒绝')])),
                ('AssessTime', models.DateTimeField(auto_now_add=True)),
                ('Notes', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=18)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='assessinfo',
            name='AssessorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assesses.Assessor'),
        ),
        migrations.AddField(
            model_name='assessinfo',
            name='RestaurantID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApplyController.Restaurant'),
        ),
    ]
