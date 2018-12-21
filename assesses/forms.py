from django import forms
from .models import Assessor


class AccessForm(forms.ModelForm):
    class Meta:
        model = Assessor
        fields = ("name", 'password')
        labels = {"username": "用户名:", "password": "密码："}
