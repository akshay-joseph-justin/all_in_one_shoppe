from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('shop/', views.ShopListView.as_view(), name="shop"),
    path('shop/', views.ShopListImageView.as_view(), name="shop-image"),
    path('shop/<slug>', views.ProductDetailView.as_view(), name="product-detail"),
    path('shop/<slug>', views.ProductImageView.as_view(), name="product-detail-image"),
]
