from django.shortcuts import render
from . import forms
from .models import User,CouponPurchase,Review,Order,OrderDetail
from ApplyController.models import Restaurant
from ManagementController.models import Coupon,Dish
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
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    dishes = Dish.objects.filter(RestaurantID=restaurant)
    if request.method!="POST":
        carts = request.session.get("carts", None)
        if not carts:
            carts = {dish.Name:0 for dish in dishes}
            request.session["carts"] = carts
        context = {"dishes": dishes,"carts":carts}
        print(carts)
        return render(request,"UserController/order.html",context=context)
    pass


def review(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    if request.method!="POST":
        form = forms.ReviewForm()
    else:
        form = forms.ReviewForm(data=request.POST)
        new_review = form.save(commit=False)
        new_review.RestaurantID = restaurant
        new_review.UserID = User.objects.get(ID=request.session["user"])
        new_review.ThumbUpCount = 0
        new_review.save()
        new_review.save()
        return HttpResponseRedirect(reverse("UserController:recommend",args={restaurant_id}))
    context = {"form":form,"restaurant":restaurant}
    return render(request,"UserController/review.html",context)


@ csrf_exempt
def recommend(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    dishes = Dish.objects.filter(RestaurantID=restaurant)
    if request.method!="POST":
        return render(request,"UserController/recommend.html",context={"dishes":dishes,"restaurant":restaurant})
    else:
        check_box_lists = request.POST.getlist("check_box_list")
        user = User.objects.get(ID=request.session["user"])
        for dish_id in check_box_lists:
            dish_id = int(dish_id)
            dish = Dish.objects.get(ID=dish_id)
            dish.RecommendCount = dish.RecommendCount+1
            dish.save()
            user.UserRecommend.add(dish)
            user.save()
        return HttpResponseRedirect(reverse("UserController:detail",args={restaurant_id}))

@ csrf_exempt
def add(request):
    dish_id = request.POST.get("id")
    dish = Dish.objects.get(ID=dish_id)
    carts = request.session["carts"]
    carts[dish.Name]+=1
    request.session["carts"] = carts
    return JsonResponse({"status":"ok","num":carts[dish.Name]})


@ csrf_exempt
def minus(request):
    dish_id = request.POST.get("id")
    dish = Dish.objects.get(ID=dish_id)
    carts = request.session["carts"]
    if carts[dish.Name]>0:
        carts[dish.Name]-=1
    request.session["carts"] = carts
    return JsonResponse({"status":"ok","num":carts[dish.Name]})


def confirm_order(request):
    carts = request.session["carts"]
    temp = []
    for cart in carts:
        dish = Dish.objects.filter(Name=cart)[0]
        temp.append(dish)
    restaurant = temp[0].RestaurantID

    v = 0
    count = 0
    for cart in carts:
        v+=carts[cart]*temp[count].Price
        count+=1
    context = {"dishes": temp, "carts": carts,"value":v,"restaurant":restaurant}

    return render(request,"UserController/confirm_order.html",context=context)


@ csrf_exempt
def confirm(request):
    restaurant_id = request.POST.get("id")
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    new_order = Order()
    new_order.RestaurantID = restaurant
    new_order.UserID = User.objects.get(ID=request.session["user"])
    new_order.Notes = request.POST.get("note")
    new_order.save()

    carts = request.session["carts"]
    temp = []
    for cart in carts:
        dish = Dish.objects.filter(Name=cart)[0]
        temp.append(dish)

    for dish in temp:
        new_oder_detail = OrderDetail()
        new_oder_detail.OrderID = new_order
        new_oder_detail.DishID = dish
        new_oder_detail.Amount = carts[dish.Name]
        new_oder_detail.save()
    return JsonResponse({"status":"ok"})
