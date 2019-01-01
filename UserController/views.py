from django.shortcuts import render, get_object_or_404
from . import forms
from .models import *
from ManagementController.models import *
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import datetime
from ManagementController.views import table_status_cal
import pytz


# Create your views here.
def index(request):
    restaurants = Restaurant.objects.order_by("Name")
    context = {"restaurants": restaurants}
    return render(request, "UserController/index.html", context=context)


def login(request):
    if request.method != "POST":
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = User.objects.filter(Name=request.POST["Name"], Password=request.POST["Password"])
            if user:
                request.session["user"] = user[0].id
                request.session["user_name"] = user[0].Name
                return HttpResponseRedirect(reverse("UserController:index"))
            else:
                return HttpResponseRedirect(reverse("UserController:login"))
    context = {"form": form}
    return render(request, "UserController/login.html", context)


def logout(request):
    del request.session["user"]
    del request.session["user_name"]
    return HttpResponseRedirect(reverse("UserController:login"))


def register(request):
    if request.method != "POST":
        form = forms.UserForm()
    else:
        form = forms.UserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session["user"] = new_user.id
            return render(request, "UserController/jump.html", context={"new_user":new_user})
    context = {"form": form}
    return render(request, "UserController/register.html", context=context)


def detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    user = User.objects.get(id=request.session["user"])

    try:
        del request.session["carts"]
    except:
        pass

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
    restaurant = Restaurant.objects.get(id=restaurant_id)
    coupons = Coupon.objects.filter(RestaurantID=restaurant)
    return render(request,"UserController/coupon.html",context={"coupons":coupons})


@ csrf_exempt
def purchase_coupon(request):
    coupon_id = request.POST.get('id')
    coupon = Coupon.objects.get(id=coupon_id)
    if coupon.Amount>0:
        user = User.objects.get(id=request.session["user"])
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
    restaurant = Restaurant.objects.get(id=restaurant_id)
    user = User.objects.get(id=request.session["user"])
    user.Favorite.add(restaurant)
    print(user.Favorite.all())
    user.save()
    return JsonResponse({"status":"ok"})


@ csrf_exempt
def unfavorite(request):
    restaurant_id = request.POST.get("id")
    restaurant = Restaurant.objects.get(id=restaurant_id)
    user = User.objects.get(id=request.session["user"])
    user.Favorite.remove(restaurant)
    user.save()
    return JsonResponse({"status":"ok"})


@ csrf_exempt
def thump_up(request):
    review_id = request.POST.get("id")
    review = Review.objects.get(id=review_id)
    review.ThumbUpCount = review.ThumbUpCount+1
    num = str(review.ThumbUpCount)
    review.save()
    return JsonResponse({"status":"ok","num":num})


def order(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    dishes = Dish.objects.filter(RestaurantID=restaurant)

    if request.method!="POST":
        carts = request.session.get("carts", None)
        if not carts:
            carts = {dish.id:0 for dish in dishes}
            request.session["carts"] = carts
        context = {"dishes": dishes,"carts":carts,"restaurant":restaurant}
        print(carts)
        return render(request,"UserController/order.html",context=context)
    pass


def review(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method!="POST":
        form = forms.ReviewForm()
    else:
        form = forms.ReviewForm(data=request.POST)
        new_review = form.save(commit=False)
        new_review.RestaurantID = restaurant
        new_review.UserID = User.objects.get(id=request.session["user"])
        new_review.ThumbUpCount = 0
        new_review.save()
        new_review.save()
        return HttpResponseRedirect(reverse("UserController:recommend",args={restaurant_id}))
    context = {"form":form,"restaurant":restaurant}
    return render(request,"UserController/review.html",context)


@ csrf_exempt
def recommend(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    dishes = Dish.objects.filter(RestaurantID=restaurant)
    if request.method!="POST":
        return render(request,"UserController/recommend.html",context={"dishes":dishes,"restaurant":restaurant})
    else:
        check_box_lists = request.POST.getlist("check_box_list")
        user = User.objects.get(id=request.session["user"])
        for dish_id in check_box_lists:
            dish_id = int(dish_id)
            dish = Dish.objects.get(id=dish_id)
            dish.RecommendCount = dish.RecommendCount+1
            dish.save()
            user.UserRecommend.add(dish)
            user.save()
        return HttpResponseRedirect(reverse("UserController:detail",args={restaurant_id}))

@ csrf_exempt
def add(request):
    dish_id = request.POST.get("id")
    dish = Dish.objects.get(id=dish_id)
    carts = request.session["carts"]
    carts[str(dish.id)]+=1
    request.session["carts"] = carts
    return JsonResponse({"status":"ok","num":carts[str(dish.id)]})


@ csrf_exempt
def minus(request):
    dish_id = request.POST.get("id")
    dish = Dish.objects.get(id=dish_id)
    carts = request.session["carts"]
    if carts[str(dish.id)]>0:
        carts[str(dish.id)]-=1
    request.session["carts"] = carts
    return JsonResponse({"status":"ok","num":carts[str(dish.id)]})


def confirm_order(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    carts = request.session["carts"]
    temp = []
    for cart in carts:
        if carts[cart]!=0:
            dish = Dish.objects.get(id=int(cart))
            temp.append(dish)
    if temp:
        restaurant = temp[0].RestaurantID

        v = 0
        count = 0
        for cart in carts:
            v+=carts[cart]*temp[count].Price
            count+=1
        context = {"dishes": temp, "carts": carts,"value":v,"restaurant":restaurant}
        return render(request,"UserController/confirm_order.html",context=context)

    else:
        return render(request,"UserController/confirm_order.html",context={"restaurant":restaurant})

@ csrf_exempt
def confirm(request):
    restaurant_id = request.POST.get("id")
    restaurant = Restaurant.objects.get(id=restaurant_id)
    new_order = Order()
    new_order.RestaurantID = restaurant
    new_order.UserID = User.objects.get(id=request.session["user"])
    new_order.Notes = request.POST.get("note")
    new_order.save()

    carts = request.session["carts"]
    temp = []
    for cart in carts:
        dish = Dish.objects.get(id=int(cart))
        temp.append(dish)

    for dish in temp:
        print("order_detail")
        if dish.RestaurantID==restaurant:
            print("hahah")
            new_oder_detail = OrderDetail()
            new_oder_detail.OrderID = new_order
            new_oder_detail.DishID = dish
            new_oder_detail.Amount = carts[str(dish.id)]
            new_oder_detail.save()

    del request.session["carts"]

    return JsonResponse({"status":"ok"})


def make_reservation(request, restaurant_id):
    if request.method == 'POST':
        form = forms.MakeReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            date_chosen = data['date']
            meal_type = data['occupation_time']
            dining_number = data['capacity']
            if meal_type == 'lunch':
                datetime_chosen = datetime.datetime(date_chosen.year, date_chosen.month, date_chosen.day, hour=12)
            if meal_type == 'supper':
                datetime_chosen = datetime.datetime(date_chosen.year, date_chosen.month, date_chosen.day, hour=18)
            request.session['datetime_chosen'] = str(datetime_chosen)
            request.session['dining_number'] = str(dining_number)
            return HttpResponseRedirect(reverse('UserController:reserve_available', args=(restaurant_id,)))
    else:
        form = forms.MakeReservationForm()
        return render(request, "UserController/make_reservation.html", context={
            'form': form,
            'restaurant_id': restaurant_id,
        })


def reserve_available(request, restaurant_id):
    reserve_time = datetime.datetime.strptime(request.session.get('datetime_chosen'), "%Y-%m-%d %H:%M:%S")
    dining_number = request.session.get('dining_number')
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    table_list = list(Table.objects.filter(RestaurantID=restaurant).filter(Capacity__gte=int(dining_number)))
    available_table = []
    meal_type = 0  # 预约类型为中饭
    if reserve_time.hour == 18:
        meal_type = 1  # 预约类型为晚饭
    else:
        pass
    for table in table_list:
        if table_status_cal(table, reserve_time.astimezone(pytz.timezone("UTC"))) == 0:
            reserve_list = Reserve.objects.filter(TableNum=table.TableNum).filter(OccupationDate=reserve_time.date()).\
                filter(OccupationTime=meal_type)
            if not reserve_list:
                available_table.append(table)

    return render(request, 'UserController/reserve.html', context={
        'tables': available_table,
        'restaurant_id': restaurant_id
    })


def choose_reserve(request, restaurant_id):
    user_id = request.session.get('user')
    user = User.objects.get(pk=user_id)
    selected_table = get_object_or_404(Table, pk=request.POST['choice'])
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    reserve_time = datetime.datetime.strptime(request.session.get('datetime_chosen'), "%Y-%m-%d %H:%M:%S")
    reserve_date = reserve_time.date()
    reserve_type = 0  # 预约类型为中饭
    if reserve_time.hour == 18:
        reserve_type = 1  # 预约类型为晚饭
    else:
        pass
    new_reserve = Reserve(RestaurantID=restaurant,
                          TableNum=selected_table.TableNum,
                          OccupationDate=reserve_date,
                          OccupationTime=reserve_type,
                          UserID=user)
    new_reserve.save()
    reserve_id = new_reserve.id
    return HttpResponseRedirect(reverse('UserController:reserve_result', args=(restaurant_id, reserve_id,)))


def reserve_result(request, restaurant_id, reserve_id):
    restaurant_reserved = Restaurant.objects.get(pk=restaurant_id)
    reserve = Reserve.objects.get(pk=reserve_id)
    return render(request, "UserController/reserve_result.html", context={
        'reserve': reserve,
        'restaurant': restaurant_reserved,
    })


def user_info(request, user_id):
    user_login_id = request.session.get('user')
    if user_id != user_login_id or not user_login_id:
        return HttpResponseForbidden("您无权访问该用户信息！")
    else:
        user = User.objects.get(pk=user_id)
        user_reserve = user.reserve_set.all()
        user_coupon = Coupon.objects.filter(UserID=user)
        user_order = Order.objects.filter(UserID=user)
        return render(request, "UserController/user_info.html", context={
            'user': user,
            'reservations': user_reserve,
            'coupons': user_coupon,
            'orders': user_order,
        })
