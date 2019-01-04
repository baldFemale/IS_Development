from django.shortcuts import render
from UserController.models import User
from assesses.models import Assessor
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm,UserForm

# Create your views here.


def index(request):
    login_form = LoginForm()
    user_register_form = UserForm
    context = {"login_form":login_form,"user_register_form":user_register_form}
    return render(request,"login/index.html",context=context)


def login(request):
    account = request.POST.get("radio")
    if account=="1":
        user = User.objects.filter(Name=request.POST["account"], Password=request.POST["password"])
        if user:
            request.session["user"] = user[0].id
            request.session["user_name"] = user[0].Name
            return HttpResponseRedirect(reverse("UserController:index"))
        else:
            return HttpResponseRedirect(reverse("login:index"))
    elif account=="3":
        assess = Assessor.objects.filter(name=request.POST["account"], password=request.POST["password"])
        if assess:
            request.session["assessor"] = assess[0].id
            request.session["assessor_name"] = assess[0].name
            return HttpResponseRedirect(reverse("assesses:index"))
        else:
            return HttpResponseRedirect(reverse("login:index"))
    else:
        pass
    return HttpResponseRedirect(reverse("login:index"))


def user_register(request):
    form = UserForm(data=request.POST)
    if form.is_valid():
        new_user = User()
        new_user.Name = request.POST.get("account")
        new_user.Password = request.POST.get("password")
        new_user.Sex = request.POST.get("sex")
        new_user.PhoneNum = request.POST.get("PhoneNum")
        new_user.save()
        request.session["user"] = new_user.id
        request.session["user_name"] = new_user.Name
        return render(request, "UserController/jump.html", context={"new_user": new_user})
    pass