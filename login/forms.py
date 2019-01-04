from django import forms
from django.core.validators import MinLengthValidator, RegexValidator


class LoginForm(forms.Form):

    account_choice = (
        ('1', '用户登录'),
        ('2', '商家登录'),
        ('3', '审核员登录'),
    )
    account = forms.CharField(max_length=20,label="账号",required=True)
    password = forms.CharField(max_length=20,label="密码",widget=forms.PasswordInput,required=True,validators=[MinLengthValidator(8)])
    radio = forms.ChoiceField(choices=account_choice,initial=1,widget=forms.RadioSelect,label="身份")


class UserForm(forms.Form):

    account = forms.CharField(max_length=20,label="账号",required=True)
    password = forms.CharField(max_length=20,label="密码",widget=forms.PasswordInput,required=True,validators=[MinLengthValidator(8)])
    Sex_category = (
        (0, '男'),
        (1, '女'),
    )
    sex = forms.ChoiceField(choices=Sex_category)
    PhoneNum_regex_validator = RegexValidator(regex=r'^\d{7}$', inverse_match=True)
    PhoneNum = forms.CharField(max_length=11, validators=[PhoneNum_regex_validator])

