from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('shop/', views.ShopView.as_view(), name="shop"),
]
