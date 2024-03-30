from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('shop/', views.ShopListView.as_view(), name="shop"),
    path('shop/<slug>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('cart/', views.CartListView.as_view(), name="cart-list"),
    path('cart/add/<slug>/', views.AddToCartView.as_view(), name="cart-add"),
    path('cart/remove/<slug>/', views.RemoveFromCart.as_view(), name="cart-remove"),
    path('cart/update/<pk>/<action>', views.UpdateCart.as_view(), name="cart-update"),
    path('order/', views.OrderListView.as_view(), name="order-list"),
    path('order/place/', views.PlaceOrderView.as_view(), name="order-place"),
    path('order/confirm/', views.OrderConfirmationView.as_view(), name="order-confirm"),
    path('order/detail/<slug>/', views.OrderDetailView.as_view(), name="order-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)