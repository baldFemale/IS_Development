from django.shortcuts import render
from assesses import forms
from assesses.models import Assessor,AssessInfo
from django.http import HttpResponseRedirect
from django.urls import reverse
from ApplyController.models import Restaurant

# Create your views here.

def index(request):
    assessinfos = AssessInfo.objects.order_by("AssessTime")
    context = {"assessor":request.session["assessor"],"assessinfos":assessinfos}
    return render(request,"assesses/index.html",context)


def login(requset):
    if requset.method!="POST":
        form = forms.AccessorForm()
    else:
        form = forms.AccessorForm(data=requset.POST)
        if form.is_valid():
            name = requset.POST["name"]
            password = requset.POST["password"]
            assess = Assessor.objects.filter(name=name,password=password)
            if assess:
                requset.session["assessor"] = assess[0].name
                return HttpResponseRedirect(reverse("assesses:index"))
            else:
                return HttpResponseRedirect(reverse("assesses:login"))
    context ={"form":form}
    return render(requset,"assesses/login.html",context)

def detail(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    context = {"assessor":request.session["assessor"],"restaurant":restaurant}
    return render(request,"assesses/detail.html",context)

