from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(CouponPurchase)
# Register your models here.
