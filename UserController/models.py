from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from ApplyController.models import Merchant
from ManagementController.models import Dish, Restaurant, Coupon


class User(models.Model):
    # ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)
    # 密码长度至少8位
    Password = models.CharField(max_length=20, validators=[MinLengthValidator(8)])
    Sex_category = (
        (0, '男'),
        (1, '女'),
    )
    Sex = models.PositiveSmallIntegerField(choices=Sex_category)
    PhoneNum_regex_validator = RegexValidator(regex=r'^\d{7}$', inverse_match=True)
    PhoneNum = models.CharField(max_length=11, validators=[PhoneNum_regex_validator])
    Favorite = models.ManyToManyField(Restaurant)
    UserRecommend = models.ManyToManyField(Dish)

    def __str__(self):
        return self.Name


class Review(models.Model):
    # ID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Score_category = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    Score = models.PositiveSmallIntegerField(choices=Score_category)
    Content = models.CharField(max_length=500)
    ThumbUpCount = models.PositiveIntegerField()
    ReviewTime = models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    # ID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    OrderTime = models.DateTimeField(auto_now_add=True)
    Notes = models.CharField(max_length=100, null=True)


class OrderDetail(models.Model):
    # ID = models.AutoField(primary_key=True)
    OrderID = models.ForeignKey(Order,
                                on_delete=models.CASCADE,)
    DishID = models.ForeignKey(Dish, on_delete=models.CASCADE)
    Amount = models.PositiveSmallIntegerField()


class CouponPurchase(models.Model):
    # ID = models.AutoField(primary_key=True)
    CouponID = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    BuyTime = models.DateTimeField(auto_now_add=True)

