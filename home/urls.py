from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('login/pppp', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
