from django import forms
from .models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["Name","Password"]
        labels = {"Name":"账号","Password":"密码"}

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ["Name","Password","Sex","PhoneNum"]
        labels = {"Name":"姓名","Password":"密码","Sex":"性别","电话":"PhoneNum"}