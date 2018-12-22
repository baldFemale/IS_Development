from django import forms
from .models import Assessor,AssessInfo


class AccessorForm(forms.ModelForm):
    class Meta:
        model = Assessor
        fields = ("name", 'password')
        labels = {"username": "用户名:", "password": "密码："}

# class AssessForm(forms.ModelForm):
#     class Meta:
#         model = AssessInfo

