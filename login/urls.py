from . import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    # 主页
    url(r"^index/$",views.index,name="index"),
    # 登录
    url(r"^login/$",views.login,name="login"),
    # 用户注册
    url(r"^user_register/$", views.user_register, name="user_register"),
    ]