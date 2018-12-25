from django.shortcuts import render
from ApplyController.models import Restaurant
from . import forms
from .models import Dish,Coupon
from UserController.models import Review
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
