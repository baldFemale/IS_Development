from django.urls import path

from . import views

app_name = 'apply'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:restaurant_id>/edit/', views.edit, name='edit'),
    path('add/', views.add_restaurant, name='add'),
]
