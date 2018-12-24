from django import forms
from .models import Restaurant,Coupon,Dish


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["Name","BusinessStartHour","BusinessEndHour","Address","Image","Category"]
        labels = {
            "Name": "商家名称",
            "BusinessStartHour": "开始营业时间",
            "BusinessEndHour": "结束营业时间",
            "Address": "地址",
            "Image": "图片",
            "Category":"类型",
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["Name","Price","Value","Amount","Notes"]
        labels = {
            "Name":"优惠券名称",
            "Price":"价格",
            "Value":"价值",
            "Amount":"数量",
            "Notes":"备注",
        }


class DishForm(forms.ModelForm):

    class Meta:
        model =Dish
        fields = ["Name","Price","Image","Type"]
        labels = {
            "Name":"菜品名称",
            "Price":"价格",
            "Image":"图片",
            "Type":"类型",
        }

