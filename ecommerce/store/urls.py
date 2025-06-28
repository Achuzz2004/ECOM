from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),  
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order-history'),
    path('payment/',views.payment, name='payment'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
