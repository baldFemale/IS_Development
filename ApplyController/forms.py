from .models import Restaurant
from django import forms


class MerchantForm(forms.Form):
    Name = forms.CharField(max_length=20, label='用户名')
    Password = forms.CharField(max_length=20, label='密码')


class RestaurantEditForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['Name', 'BusinessStartHour', 'BusinessEndHour', 'Address', 'Category', 'Image']

    def __init__(self, *args, **kwargs):
        super(RestaurantEditForm, self).__init__(*args, **kwargs)
        for field_name in ['Name', 'BusinessStartHour', 'BusinessEndHour', 'Address', 'Category', 'Image']:
            self.base_fields[field_name].widget.attrs.update({'class': 'from-control'})


class RestaurantAddForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['Name', 'BusinessStartHour', 'BusinessEndHour', 'Address', 'Category', 'LicenseID']
