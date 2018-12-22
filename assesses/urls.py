from django.conf.urls import url
from . import views

urlpatterns =[
    # 主页
    url(r"^$",views.index,name="index"),
    url(r"^login/$",views.login,name="login"),
    # url(r"^logout/$",views.logout,name="logout"),
    url(r'^detail/(?P<restaurant_id>\d+)/$',views.detail,name="detail"),
]
