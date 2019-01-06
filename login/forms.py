from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from ApplyController.models import Merchant
from django.forms import widgets as wid


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
    sex = forms.ChoiceField(choices=Sex_category, label='性别')
    PhoneNum_regex_validator = RegexValidator(regex=r'^\d{7}$', inverse_match=True)
    PhoneNum = forms.CharField(max_length=11, validators=[PhoneNum_regex_validator], label='手机号码')


class MerchantRegisterForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = '__all__'
        labels = {'IdentityNum': '身份证号码',
                  'PhoneNum': '手机号码', }
        widgets = {
            'Password': wid.PasswordInput()
        }
