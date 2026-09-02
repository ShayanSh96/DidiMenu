from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('story/', views.story, name='story'),
    path('family/', views.family, name='family'),
    path('menu/', views.menu_home, name='home'),
    path('menu/<slug:slug>/', views.item_detail, name='item_detail'),
]
