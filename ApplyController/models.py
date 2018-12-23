from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import time


def validate_identity_num(char):
    if len(char) != 18:
        raise ValidationError(
            _('身份证长度不合法.')
        )


class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    # 密码长度至少8位
    Password = models.CharField(max_length=20, validators=[MinLengthValidator(8)], verbose_name='密码')
    # 身份证长度固定为18位
    IdentityNum = models.CharField(validators=[validate_identity_num], max_length=20)

    PhoneNum_regex_validator = RegexValidator(regex=r'^\d{7}$', inverse_match=True)
    PhoneNum = models.CharField(max_length=11, validators=[PhoneNum_regex_validator])

    def __str__(self):
        return self.Name


def get_file_path(instance, filename):
    # 设置Restaurant的Image的上传路径
    sub = filename.split('.')[-1]
    t = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return 'image/%s/avatar/%s.%s' % (instance.MerchantID, t, sub,)


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    MerchantID = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    BusinessStartHour = models.TimeField()
    BusinessEndHour = models.TimeField()
    Address = models.CharField(max_length=50)
    Image = models.ImageField(upload_to=get_file_path, null=True)
    Score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    Category_Choices = (
        ('1', '川菜'),
        ('2', '粤菜'),
        ('3', '鲁菜'),
        ('4', '苏菜'),
        ('5', '湘菜'),
        ('6', '浙菜'),
        ('7', '其他'),
    )
    Category = models.CharField(max_length=1, choices=Category_Choices)
    LicenseID = models.CharField(validators=[RegexValidator(regex='^[0-9]*$')], max_length=50)
    ApplicationTime = models.DateTimeField(auto_now_add=True)

    Status_Choices = (
        (0, '待审核'),
        (1, '审核拒绝'),
        (2, '审核通过'),
    )
    Status = models.SmallIntegerField(choices=Status_Choices, default=0)
    OpenTime = models.DateTimeField(null=True)

    def __str__(self):
        return self.Name

