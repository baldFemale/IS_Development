from django import forms
from .models import Assess

class AccessForm(forms.ModelForm):
    class Meta:
        model = Assess
        fields = ("name",'password')
        labels = {"username":"用户名:","password":"密码："}