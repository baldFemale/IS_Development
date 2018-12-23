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
    url(r"^purchase_coupon/$",views.purchase_coupon,name="purchase_coupon"),
    # 预点餐界面
    url(r"^order/(?P<restaurant_id>\d)/$",views.order,name="order"),
    # 评论界面
    url(r"^review/(?P<restaurant_id>\d)/$",views.review,name="review"),
    # 收藏
    url(r"^favorite/$",views.favorite,name="favorite"),
    # 取消收藏
    url(r"^unfavorite/$", views.unfavorite, name="unfavorite"),
    # 点赞
    url(r"^thump_up/$",views.thump_up,name="thump_up"),
]