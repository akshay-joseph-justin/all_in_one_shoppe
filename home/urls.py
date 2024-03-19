from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('product/', views.product),
    path('cart/', views.cart),
    path('login/pppp', views.login),
]
