from django.shortcuts import render
from . import forms
from .models import User,CouponPurchase,Review
from ApplyController.models import Restaurant
from ManagementController.models import Coupon
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

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
    user = User.objects.get(ID=request.session["user"])

    favorite = 0
    if restaurant in user.Favorite.all():
            print("hahahahahaha")
            favorite = 1

    reviews = Review.objects.filter(RestaurantID=restaurant)
    limit = 4
    paginator = Paginator(reviews,limit)
    page = request.GET.get('page',1)
    result = paginator.page(page)

    context = {"restaurant": restaurant, "coupons": coupons,"favorite":favorite,"result":result}
    return render(request,"UserController/detail.html",context=context)


def coupon(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    return render(request,"UserController/coupon.html",context={"coupons":coupons})


@ csrf_exempt
def purchase_coupon(request):
    coupon_id = request.POST.get('id')
    coupon = Coupon.objects.get(ID=coupon_id)
    if coupon.Amount>0:
        user = User.objects.get(ID=request.session["user"])
        coupon_parchase = CouponPurchase(CouponID=coupon,UserID=user)
        coupon_parchase.save()
        coupon.Amount = coupon.Amount-1
        coupon.save()
        return JsonResponse({"status":"ok","amount":str(coupon.Amount)})
    else:
        return JsonResponse({"status":"fail"})


@ csrf_exempt
def favorite(request):
    restaurant_id = request.POST.get("id")
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    user = User.objects.get(ID=request.session["user"])
    user.Favorite.add(restaurant)
    print(user.Favorite.all())
    user.save()
    return JsonResponse({"status":"ok"})


@ csrf_exempt
def unfavorite(request):
    restaurant_id = request.POST.get("id")
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    user = User.objects.get(ID=request.session["user"])
    user.Favorite.remove(restaurant)
    user.save()
    return JsonResponse({"status":"ok"})


@ csrf_exempt
def thump_up(request):
    review_id = request.POST.get("id")
    review = Review.objects.get(ID=review_id)
    review.ThumbUpCount = review.ThumbUpCount+1
    num = str(review.ThumbUpCount)
    review.save()
    return JsonResponse({"status":"ok","num":num})


def order(request,restaurant_id):
    pass

def review(request,restaurant_id):
    pass


