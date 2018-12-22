from . import views
from django.conf.urls import url

urlpatterns = [
    # 主页
    url(r"^index/$",views.index,name="index"),
    # 注册
    url(r"^register/$",views.register,name="register"),
    # 登录
    url(r"^login/$",views.login,name="login"),
    # 注销
    # url(r"^logout/$",views.logout,name="logout"),
    # 详细页
    url(r"^detail/(?P<restaurant_id>\d)/$",views.detail,name="detail"),
    # 优惠券界面
    url(r"^coupon/(?P<restaurant_id>\d)/$",views.coupon,name="coupon"),
    # 购买优惠券
    # url(r"^purchase_coupon/(?P<coupon_id>\d)/$",views,name="purchase_coupon"),
]