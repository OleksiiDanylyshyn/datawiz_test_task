from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('key_indicators/', views.key_indicators, name='key_indicators'),
    path('products_increase/', views.products_increase, name='products_increase'),
    path('get_products/', views.get_products, name='get_products'),
    path('products_decrease/', views.products_decrease, name='products_decrease'),
]
