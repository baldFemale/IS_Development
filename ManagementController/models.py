from django.db import models
from ApplyController.models import Restaurant
import time
from django.utils import timezone


class Table(models.Model):
    # ID = models.AutoField(primary_key=True)
    TableNum = models.PositiveSmallIntegerField()
    RestaurantID = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    Capacity = models.PositiveSmallIntegerField()
    CloseTime = models.DateTimeField(null=True, blank=True)
    OpenTime = models.DateTimeField(default=timezone.now())

    Status_Choice = (
        (0, '开放'),
        (1, '待关闭'),
        (2, '待关闭/开放'),
        (3, '关闭'),
        (4, '待开放'),
    )
    # TO-DO 计算列
    Status = models.PositiveSmallIntegerField(choices=Status_Choice, blank=True, null=True)


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
    Image = models.ImageField(upload_to=get_file_path, blank=True, null=True)

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


