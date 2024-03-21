from django.urls import path

from . import (
    views,
    product_views,
    category_views,
    discount_view,
    image_views,
    order_views,
    review_views,
    cart_views
)

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name="home"),
]

product_patterns = [
    path('products/', product_views.ProductListView.as_view(), name="product-list"),
    path('products/<slug>/', product_views.ProductDetailView.as_view(), name="product-detail"),
    path('products/add/', product_views.ProductAddView.as_view(), name="product-add"),
    path('products/update/<slug>/', product_views.ProductUpdateView.as_view(), name="product-update"),
    path('products/delete/<slug>/', product_views.ProductDeleteView.as_view(), name="product-delete"),
]

category_patterns = [
    path('category/', category_views.CategoryListView.as_view(), name="category-list"),
    path('category/<slug>/', category_views.CategoryDetailView.as_view(), name="category-detail"),
    path('category/add/', category_views.CategoryAddView.as_view(), name="category-add"),
    path('category/update/<slug>/', category_views.CategoryUpdateView.as_view(), name="category-update"),
    path('category/delete/<slug>/', category_views.CategoryDeleteView.as_view(), name="category-delete"),
]

image_patterns = [
    path('image/', image_views.ImageListView.as_view(), name="image-list"),
    path('image/<slug>/', image_views.ImageDetailView.as_view(), name="image-detail"),
    path('image/add/', image_views.ImageAddView.as_view(), name="image-add"),
    path('image/update/<slug>/', image_views.ImageUpdateView.as_view(), name="image-update"),
    path('image/delete/<slug>/', image_views.ImageDeleteView.as_view(), name="image-delete"),
]

order_patterns = [
    path('order/', order_views.OrderListView.as_view(), name="order-list"),
    path('order/<slug>/', order_views.OrderDetailView.as_view(), name="order-detail"),
    path('order/delete/<slug>/', order_views.OrderDeleteView.as_view(), name="order-delete"),
]


review_patterns = [
    path('review/', review_views.ReviewListView.as_view(), name="review-list"),
    path('review/<slug>/', review_views.ReviewDetailView.as_view(), name="review-detail"),
    path('review/delete/<slug>/', review_views.ReviewDeleteView.as_view(), name="review-delete"),
]

cart_patterns = [
    path('cart/', cart_views.CartListView.as_view(), name="review-list"),
    path('cart/<slug>/', cart_views.CartDetailView.as_view(), name="review-detail"),
    path('cart/delete/<slug>/', cart_views.CartDeleteView.as_view(), name="review-delete"),
]

urlpatterns += product_patterns + category_patterns + image_patterns + order_patterns + review_patterns
