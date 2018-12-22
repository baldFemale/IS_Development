from django.shortcuts import render
from . import forms
from .models import User
from ApplyController.models import Restaurant
from ManagementController.models import Coupon
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    restaurants = Restaurant.objects.order_by("Name")
    context = {"restaurants":restaurants}
    return render(request,"UserController/index.html",context=context)


def login(request):
    if request.method!="POST":
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = User.objects.filter(Name=request.POST["Name"],Password=request.POST["Password"])
            if user:
                request.session["user"] = user[0].ID
                return HttpResponseRedirect(reverse("UserController:index"))
            else:
                return HttpResponseRedirect(reverse("UserController:login"))
    context = {"form":form}
    return render(request,"UserController/login.html",context)


def register(request):
    if request.method!="POST":
        form = forms.UserForm()
    else:
        form = forms.UserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session["user"] = new_user.ID
            return render(request,"UserController/jump.html",context={"new_user":new_user})
    context = {"form":form}
    return render(request,"UserController/register.html",context=context)


def detail(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    context = {"restaurant":restaurant,"coupons":coupons}
    return render(request,"UserController/detail.html",context=context)


def coupon(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    return render(request,"UserController/coupon.html",context={"coupons":coupons})


# def purchase_coupon(request,coupon_id):
#     _coupon = Coupon.objects.get(ID=coupon_id)
#     _coupon.Amount-=1
#     _coupon.save()
#     restaurant = Restaurant.objects.get(ID=_coupon.RestaurantID)
#     coupons = Coupon.objects.filter(RestaurantID=restaurant)
#     return render(request,"UserController/coupon.html",context={"coupons":coupons})



