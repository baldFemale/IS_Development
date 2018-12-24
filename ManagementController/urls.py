from . import views
from django.conf.urls import url

urlpatterns = [
    #主页
    url(r"^index/$",views.index,name="index"),
    #商家详细页
    url(r"^detail/(?P<restaurant_id>\d)/$",views.detail,name="detail"),
    #商家菜品
    url(r"^dish/(?P<restaurant_id>\d)/$",views.dish,name="dish"),
    #商家优惠券
    url(r"^coupon/(?P<restaurant_id>\d)/$",views.coupon,name="coupon"),
    # 修改商家菜品
    url(r"^edit_dish/(?P<dish_id>\d)/$",views.edit_dish,name="edit_dish"),
]