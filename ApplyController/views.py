from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import Merchant, Restaurant
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from django.views import generic


def index(request):
    login_user_id = request.session.get('login_merchant')
    if login_user_id:
        login_user_name = Merchant.objects.get(pk=login_user_id)
        apply_list = Restaurant.objects.filter(MerchantID=login_user_id).order_by('ApplicationTime')
        return render(request, 'ApplyController/index.html', context={
            'apply_list': apply_list,
            'login_user_name': login_user_name,
        })
    else:
        return HttpResponseRedirect(reverse('login:index'))


def login(request):
    login_merchant_id = request.session.get('login_merchant')
    if not login_merchant_id:
        if request.method == 'POST':
            form = MerchantForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user_name = data['Name']
                user_password = data['Password']
                login_merchant = Merchant.objects.filter(Name=user_name, Password=user_password)
                if login_merchant:
                    request.session['login_merchant'] = login_merchant[0].id
                    request.session['login_merchant_name'] = get_object_or_404(Merchant, pk=login_merchant[0].id).Name
                    return HttpResponseRedirect(reverse('apply:index'))
                else:
                    return render(request, 'ApplyController/login.html', context={
                        'error_message': "用户名或密码错误",
                        'form': form,
                    })
            else:
                return render(request, 'ApplyController/login.html', context={
                    'error_message': "用户名或密码错误",
                    'form': form,
                })
        else:
            form = MerchantForm()
            return render(request, 'ApplyController/login.html', context={
                'form': form,
            })
    else:
        return HttpResponseRedirect(reverse('apply:index'))


def logout(request):
    request.session.pop('login_merchant')
    return HttpResponseRedirect(reverse('apply:index'))


class DetailView(generic.DetailView):
    model = Restaurant
    template_name = 'ApplyController/detail.html'


def edit(request, restaurant_id):
    login_merchant_id = request.session.get('login_merchant')
    if login_merchant_id:
        restaurant_obj = Restaurant.objects.get(pk=restaurant_id)
        if request.method == 'POST':
            form = RestaurantEditForm(request.POST, request.FILES, instance=restaurant_obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('apply:detail', args=(restaurant_id,)))
            else:
                return render(request, "ApplyController/edit.html", context={
                    'error_message': '修改不成功',
                })
        else:
            form = RestaurantEditForm(instance=restaurant_obj)
        return render(request, 'ApplyController/edit.html', context={
            'restaurant_edit_form': form,
            'error_message': '修改成功',
        })
    else:
        return HttpResponseRedirect(reverse('login:index'))


def add_restaurant(request):
    login_merchant_id = request.session.get('login_merchant')
    if login_merchant_id:
        if request.method == 'POST':
            form = RestaurantAddForm(request.POST)
            if form.is_valid():
                new_restaurant = form.save(commit=False)
                new_restaurant.MerchantID = Merchant.objects.get(pk=login_merchant_id)
                new_restaurant.save()
                return index(request)
            else:
                return render(request, 'ApplyController/add.html', context={
                    'form': form,
                    'error_message': '添加失败'
                })
        else:
            form = RestaurantAddForm()
            return render(request, 'ApplyController/add.html', context={
                'form': form,
            })
    else:
        return HttpResponseRedirect(reverse('login:index'))


def register(request):
    login_merchant_id = request.session.get('login_merchant')
    if login_merchant_id:
        return index(request)
    else:
        if request.method == 'POST':
            form = MerchantRegisterForm(request.POST)
            if form.is_valid():
                new_merchant = form.save(commit=False)
                request.session['login_merchant'] = new_merchant.id
                new_merchant.save()
                return render(request, 'ApplyController/index.html', context={'error_message': '注册成功'})
            else:
                return render(request, 'ApplyController/register.html', context={
                    'error_message': '注册失败',
                    'form': form,
                })
        else:
            form = MerchantRegisterForm()
            return render(request, 'ApplyController/register.html', context={
                'form': form,
            })


def merchant_detail(request):
    merchant_id = request.session.get('login_merchant')
    if merchant_id:
        merchant = Merchant.objects.get(pk=merchant_id)
        return render(request, 'ApplyController/merchant.html', context={'merchant': merchant})
    else:
        return HttpResponseNotAllowed()
