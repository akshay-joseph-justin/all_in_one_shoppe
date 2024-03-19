from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('product/', views.product),
    path('cart/', views.cart, name="cart"),
]
