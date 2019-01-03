from .models import Restaurant, Merchant
from django import forms
from django.forms import widgets as wid


class MerchantForm(forms.Form):
    Name = forms.CharField(max_length=20, label='用户名')
    Password = forms.CharField(max_length=20, label='密码')


class RestaurantEditForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['Name', 'BusinessStartHour', 'Image', 'BusinessEndHour', 'Address', 'Category', ]
        labels = {'Name': '餐厅名称',
                  'Image': '餐厅图片',
                  'BusinessStartHour': '开始营业时间',
                  'BusinessEndHour': '结束营业时间',
                  'Address': '餐厅地址',
                  'Category': '餐厅类型',}

    def __init__(self, *args, **kwargs):
        super(RestaurantEditForm, self).__init__(*args, **kwargs)
        for field_name in ['Name', 'BusinessStartHour', 'BusinessEndHour', 'Address', 'Category', 'Image']:
            self.base_fields[field_name].widget.attrs.update({'class': 'from-control'})


class RestaurantAddForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['Name', 'Image', 'BusinessStartHour', 'BusinessEndHour', 'Address', 'Category', 'LicenseID']
        labels = {'Name': '餐厅名称',
                  'Image': '餐厅图片',
                  'BusinessStartHour': '开始营业时间',
                  'BusinessEndHour': '结束营业时间',
                  'Address': '餐厅地址',
                  'Category': '餐厅类型',
                  'LicenseID': '营业执照号码',
                  }


class MerchantRegisterForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = '__all__'
