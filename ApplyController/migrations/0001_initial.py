# Generated by Django 2.1.4 on 2018-12-23 16:07

import ApplyController.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('Password', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='密码')),
                ('IdentityNum', models.CharField(max_length=20, validators=[ApplyController.models.validate_identity_num])),
                ('PhoneNum', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(inverse_match=True, regex='^\\d{7}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=20)),
                ('BusinessStartHour', models.TimeField()),
                ('BusinessEndHour', models.TimeField()),
                ('Address', models.CharField(max_length=50)),
                ('Image', models.ImageField(null=True, upload_to=ApplyController.models.get_file_path)),
                ('Score', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('Category', models.CharField(choices=[('1', '川菜'), ('2', '粤菜'), ('3', '鲁菜'), ('4', '苏菜'), ('5', '湘菜'), ('6', '浙菜'), ('7', '其他')], max_length=1)),
                ('LicenseID', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9]*$')])),
                ('ApplicationTime', models.DateTimeField(auto_now_add=True)),
                ('Status', models.SmallIntegerField(choices=[(0, '待审核'), (1, '审核拒绝'), (2, '审核通过')], default=0)),
                ('OpenTime', models.DateTimeField(null=True)),
                ('MerchantID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApplyController.Merchant')),
            ],
        ),
    ]
