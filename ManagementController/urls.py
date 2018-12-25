from . import views
from django.conf.urls import url
from django.urls import path

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
    # 增加商家菜品
    url(r"^add_dish/(?P<restaurant_id>\d)/$", views.add_dish, name="add_dish"),
    # 修改商家菜品
    url(r"^edit_coupon/(?P<coupon_id>\d)/$", views.edit_coupon, name="edit_coupon"),
    # 增加商家菜品
    url(r"^add_coupon/(?P<restaurant_id>\d)/$", views.add_coupon, name="add_coupon"),
    # 商家评论
    url(r"^review/(?P<restaurant_id>\d)/$", views.review, name="review"),
    # 显示桌位列表
    url(r"^table_info/(?P<restaurant_id>\d)/$", views.table_info, name='table_info'),
    # 显示桌位详细信息
    url(r"table_detail/(?P<table_id>\d)/$", views.table_detail, name="table_detail")
]