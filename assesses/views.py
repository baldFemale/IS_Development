from django.shortcuts import render
from assesses import forms
from assesses.models import Assessor
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request,"assesses/index.html")


def login(request):
    if request.method != "POST":
        form = forms.AccessForm()
    else:
        form = forms.AccessForm(data=request.POST)
        if form.is_valid():
            name = request.POST["name"]
            password = request.POST["password"]
            assess = Assessor.objects.filter(name=name,password=password)
            if assess:
                return HttpResponseRedirect(reverse("assesses:index"))
            else:
                return HttpResponseRedirect(reverse("assesses:login"))
    context ={"form":form}
    return render(request,"assesses/login.html",context)

