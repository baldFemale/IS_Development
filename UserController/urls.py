from . import views
from django.conf.urls import url

urlpatterns = [
    # 主页
    url(r"^index/$",views.index,name="index"),
    # 主页排序,
    url(r"^sort_index/$", views.sort_index, name="sort_index"),
    # 主页排序_开张时间,
    url(r"^sort_index_by_open_time/$", views.sort_index_by_open_time, name="sort_index_by_open_time"),
    # 主页筛选
    url(r"^sort_index_by_category/$", views.sort_index_by_category, name="sort_index_by_category"),
    # 注册
    url(r"^register/$",views.register,name="register"),
    # 登录
    url(r"^login/$",views.login,name="login"),
    # 注销
    url(r"^logout/$",views.logout,name="logout"),
    # 详细页
    url(r"^detail/(?P<restaurant_id>\d*)/$",views.detail,name="detail"),
    # 优惠券界面
    url(r"^coupon/(?P<restaurant_id>\d*)/$",views.coupon,name="coupon"),
    # 购买优惠券
    url(r"^purchase_coupon/$",views.purchase_coupon,name="purchase_coupon"),
    # 预点餐界面
    url(r"^order/(?P<restaurant_id>\d*)/$",views.order,name="order"),
    # 评论界面
    url(r"^review/(?P<restaurant_id>\d*)/$",views.review,name="review"),
    # 收藏
    url(r"^favorite/$",views.favorite,name="favorite"),
    # 取消收藏
    url(r"^unfavorite/$", views.unfavorite, name="unfavorite"),
    # 点赞
    url(r"^thump_up/$",views.thump_up,name="thump_up"),
    # 推荐
    url(r"^recommend/(?P<restaurant_id>\d*)/$", views.recommend, name="recommend"),
    # 添加菜品
    url(r"^add/$",views.add,name="add"),
    # 减少菜品
    url(r"^minus/$", views.minus, name="minus"),
    # 下单
    url(r"^confirm_order/(?P<restaurant_id>\d*)/$",views.confirm_order,name="confirm_order"),
    # 确认
    url(r"^confirm/$", views.confirm, name="confirm"),
    # 输入预约时间
    url(r"^make_reservation/(?P<restaurant_id>\d*)/$", views.make_reservation, name="make_reservation"),
    # 可预约桌位
    url(r"^reserve_available/(?P<restaurant_id>\d*)/$", views.reserve_available, name="reserve_available"),
    # 选择预约
    url(r"^choose_reserve/(?P<restaurant_id>\d*)/$", views.choose_reserve, name='choose_reserve'),
    # 预约结果
    url(r"^reserve_result/(?P<restaurant_id>\d*)/(?P<reserve_id>\d*)/$", views.reserve_result, name='reserve_result'),
    # 用户个人信息
    url(r"^user_info/(?P<user_id>\d*)/$", views.user_info, name='user_info'),
]