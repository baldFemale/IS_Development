from django import forms
from .models import *


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


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['TableNum', 'Capacity', 'CloseTime', 'OpenTime']
        labels = {
            'TableNum': '桌位号',
            'Capacity': '桌位容量',
            'CloseTime': '桌位关闭预订的开始时间',
            'OpenTime': '桌位开启预订的起始时间',
        }

