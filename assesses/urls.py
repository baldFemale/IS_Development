from django.conf.urls import url
from . import views

urlpatterns =[
    # 主页
    url(r"^index/$",views.index,name="index"),
    # 登录
    url(r"^login/$",views.login,name="login"),
    # 注销
    # url(r"^logout/$",views.logout,name="logout"),
    # 查看待审核餐厅详情
    url(r'^detail/(?P<restaurant_id>\d+)/$',views.detail,name="detail"),
]
