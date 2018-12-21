from django.shortcuts import render
from assesses import forms
from assesses.models import Assessor
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request,"assesses/index.html")


def login(requset):
    if requset.method!="POST":
        form = forms.AccessForm()
    else:
        form = forms.AccessForm(data=requset.POST)
        if form.is_valid():
            name = requset.POST["name"]
            password = requset.POST["password"]
            assess = Assess.objects.filter(name=name,password=password)
            print(form)
            if assess:
                return HttpResponseRedirect(reverse("assesses:index"))
            else:
                return HttpResponseRedirect(reverse("assesses:login"))
    context ={"form":form}
    return render(requset,"assesses/login.html",context)

