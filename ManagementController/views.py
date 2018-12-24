from django.shortcuts import render
from ApplyController.models import Restaurant
from . import forms
from .models import Dish,Coupon
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse

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
    context = {"dishes":dishes}
    return render(request,"ManagementController/dish.html",context=context)


def coupon(request,restaurant_id):
    restaurant =  Restaurant.objects.get(id=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    context = {"coupons":coupons}
    return render(request,"ManagementController/coupon.html",context=context)


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
            return HttpResponseRedirect(reverse("ManagementController:detail", args={restaurant_id}))
