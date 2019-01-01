from django.shortcuts import render
from ApplyController.models import Restaurant
from . import forms
from .models import *
from UserController.models import Review
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
import datetime

# Create your views here.


def index(request):
    restaurants = Restaurant.objects.filter(MerchantID=request.session["login_merchant"],Status=2)
    context = {"restaurants":restaurants}
    return render(request,"ManagementController/index.html",context=context)


def detail(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method!="POST":
        form = forms.RestaurantForm(instance=restaurant)
        context = {"restaurant":restaurant,"form":form}
        return render(request,"ManagementController/detail.html",context=context)
    else:
        form = forms.RestaurantForm(instance=restaurant, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ManagementController:detail",args={restaurant_id}))


def dish(request,restaurant_id):
    restaurant =  Restaurant.objects.get(id=restaurant_id)
    dishes = Dish.objects.filter(RestaurantID=restaurant)
    context = {"dishes":dishes,"restaurant":restaurant}
    return render(request,"ManagementController/dish.html",context=context)


def coupon(request,restaurant_id):
    restaurant =  Restaurant.objects.get(id=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    context = {"coupons":coupons,"restaurant":restaurant}
    return render(request,"ManagementController/coupon.html",context=context)


def review(request,restaurant_id):
    restaurant =  Restaurant.objects.get(id=restaurant_id)
    reviews = Review.objects.filter(RestaurantID=restaurant)
    context = {"reviews":reviews,"restaurant":restaurant}
    return render(request,"ManagementController/review.html",context=context)


def edit_dish(request,dish_id):
    dish = Dish.objects.get(id=dish_id)
    restaurant_id = dish.RestaurantID.id
    if request.method!="POST":
        form = forms.DishForm(instance=dish)
        context = {"form": form,"dish":dish}
        return render(request,"ManagementController/edit_dish.html",context=context)
    else:
        form = forms.DishForm(instance=dish,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ManagementController:dish", args={restaurant_id}))


def add_dish(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method!="POST":
        form = forms.DishForm()
    else:
        form = forms.DishForm(data=request.POST)
        print("hahahahahaha")
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            new_dish = form.save(commit=False)
            new_dish.RestaurantID = restaurant
            new_dish.RecommendCount = 0
            new_dish.save()
        return HttpResponseRedirect(reverse("ManagementController:dish", args={restaurant_id}))

    context = {"form":form,"restaurant":restaurant}
    return render(request, "ManagementController/add_dish.html", context=context)


def edit_coupon(request,coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    restaurant_id = coupon.RestaurantID.id
    if request.method!="POST":
        form = forms.CouponForm(instance=coupon)
        context = {"form": form,"coupon":coupon}
        return render(request,"ManagementController/edit_coupon.html",context=context)
    else:
        form = forms.CouponForm(instance=coupon,data=request.POST)
        print(form)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ManagementController:coupon", args={restaurant_id}))


def add_coupon(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method!="POST":
        form = forms.CouponForm()
    else:
        form = forms.CouponForm(data=request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            new_coupon = form.save(commit=False)
            new_coupon.RestaurantID = restaurant
            new_coupon.save()
        return HttpResponseRedirect(reverse("ManagementController:coupon", args={restaurant_id}))

    context = {"form":form,"restaurant":restaurant}
    return render(request, "ManagementController/add_coupon.html", context=context)


def table_info(request, restaurant_id):
    table_list = Table.objects.filter(RestaurantID__id=restaurant_id)
    restaurant_name = Restaurant.objects.get(pk=restaurant_id).Name
    return render(request, 'ManagementController/table_info.html', context={
        'table_list': table_list,
        'restaurant_name': restaurant_name,
        'restaurant_id': restaurant_id,
    })


def table_status_cal(table, time_now):
    # 桌位状态计算函数
    open_time = table.OpenTime
    close_time = table.CloseTime
    if close_time is None:
        if time_now > open_time:
            return 0
    else:
        if time_now > open_time > close_time:
            return 0
        if close_time > time_now and close_time > time_now:
            return 1
        if open_time > close_time > time_now:
            return 2
        if time_now > close_time > open_time:
            return 3
        if open_time > time_now > close_time:
            return 4


def table_detail(request, table_id):
    table_details = Table.objects.get(pk=table_id)
    return render(request, 'ManagementController/table_detail.html', context={
        'table_details': table_details,
    })


def table_edit(request, table_id):
    table_details = Table.objects.get(pk=table_id)
    restaurant_id = table_details.RestaurantID.id
    if request.method == "POST":
        form = forms.TableForm(request.POST, instance=table_details)
        if form.is_valid():
            # TO-DO 获取restaurant主键
            # table_num_list = [i['TableNum'] for i in Table.objects.filter(RestaurantID__id=)]
            new_table = form.save(commit=False)
            new_table.Status = table_status_cal(new_table, datetime.datetime.now())
            new_table.save()
            return table_info(request, restaurant_id)
        # else:
        #     return render(request, 'ManagementController/table_edit.html', context={
        #         'error_message': '桌位修改不成功',
        #     })
    else:
        form = forms.TableForm(instance=table_details)
        return render(request, 'ManagementController/table_edit.html', context={
            'error_message': '桌位修改成功',
            'form': form
        })


def table_add(request, restaurant_id):
    if request.method == 'POST':
        form = forms.TableForm(request.POST)
        if form.is_valid():
            new_table = form.save(commit=False)
            new_table.Status = table_status_cal(new_table, datetime.datetime.now())
            new_table.RestaurantID = Restaurant.objects.get(pk=restaurant_id)
            new_table.save()
            return table_info(request, restaurant_id)
    else:
        form = forms.TableForm()
        return render(request, "ManagementController/table_add.html", context={
            'form': form,
        })


