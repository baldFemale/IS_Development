from django.db import models
import sys
sys.path.append("..")

from ApplyController.models import Restaurant
import time


class Table(models.Model):
    # ID = models.AutoField(primary_key=True)
    TableNum = models.PositiveSmallIntegerField()
    RestaurantID = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    Capacity = models.PositiveSmallIntegerField()
    CloseTime = models.DateTimeField(null=True)
    OpenTime = models.DateTimeField(auto_now=True)

    Status_Choice = (
        (0, '开放'),
        (1, '待关闭'),
        (2, '待关闭/开放'),
        (3, '关闭'),
        (4, '待开放'),
    )
    # TO-DO 计算列
    Status = models.PositiveSmallIntegerField(choices=Status_Choice, default=0)


class Reserve(models.Model):
    # ReserveID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    TableNum = models.PositiveSmallIntegerField()

    Role_Category = (
        (0, '商家'),
        (1, '用户'),
    )
    Role = models.PositiveSmallIntegerField(choices=Role_Category)
    OccupationDate = models.DateTimeField(auto_now=True)

    OccupationTime_category = (
        (0, '中饭'),
        (1, '晚饭'),
        (2, '其他'),
    )
    OccupationTime = models.PositiveSmallIntegerField(choices=OccupationTime_category)
    MerchantID_or_UserID = models.CharField(max_length=50)
    ReserveTime = models.DateTimeField(auto_now_add=True)


def get_file_path(instance, filename):
    # 设置Restaurant的Image的上传路径
    sub = filename.split('.')[-1]
    t = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return 'image/%s/dish/%s.%s' % (instance.RestaurantID, t, sub,)


class Dish(models.Model):
    # ID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Price = models.FloatField()
    Image = models.ImageField(upload_to=get_file_path, null=True)

    Type_category = (
        (0, '开胃菜'),
        (1, '蔬菜'),
        (2, '肉类'),
        (3, '海鲜类'),
        (4, '汤'),
        (5, '甜品'),
        (6, '饮料'),
        (7, '其他'),
    )
    Type = models.PositiveSmallIntegerField(choices=Type_category)
    RecommendCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.Name


class Coupon(models.Model):
    # ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    Price = models.FloatField()
    Value = models.FloatField()
    Amount = models.PositiveIntegerField()
    Notes = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


