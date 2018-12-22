from django.shortcuts import render
from assesses import forms
from assesses.models import Assessor,AssessInfo
from ApplyController.models import Restaurant
from django.http import HttpResponseRedirect
from django.urls import reverse
from ApplyController.models import Restaurant

# Create your views here.

def index(request):
    restaurants = Restaurant.objects.filter(Status=0).order_by("ApplicationTime")
    context = {"assessor":request.session["assessor"],"restaurants":restaurants}
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
                requset.session["assessor"] = assess[0].ID
                return HttpResponseRedirect(reverse("assesses:index"))
            else:
                return HttpResponseRedirect(reverse("assesses:login"))
    context ={"form":form}
    return render(requset,"assesses/login.html",context)

def detail(request,restaurant_id):
    restaurant = Restaurant.objects.get(ID=restaurant_id)
    if request.method=="POST":
        form = forms.AssessForm(data=request.POST)
        if form.is_valid():
            new_assessinfo = form.save(commit=False)
            new_assessinfo.RestaurantID = restaurant
            assessor = Assessor.objects.get(ID=request.session["assessor"])
            new_assessinfo.AssessorID = assessor
            print(new_assessinfo)
            new_assessinfo.save()
            if new_assessinfo.Result==0:
                restaurant.Status = 2
            else:
                restaurant.Status = 1
            restaurant.save()
            return HttpResponseRedirect(reverse("assesses:index"))
    form = forms.AssessForm()
    context = {"form":form,"assessor":request.session["assessor"],"restaurant":restaurant}
    return render(request,"assesses/detail.html",context)

