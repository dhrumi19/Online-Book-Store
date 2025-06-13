from django.urls import path
from . import views

app_name = 'bookstore'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.book_list_view, name='book_list'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<int:cart_id>/', views.update_cart_view, name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment/success/<int:payment_id>/', views.payment_success_view, name='payment_success'),
    path('payment/failed/<int:order_id>/', views.payment_failed_view, name='payment_failed'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/', views.order_history_view, name='order_history'),
    path('track-order/<int:order_id>/', views.track_order_view, name='track_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order_view, name='cancel_order'),  # New URL for cancellation
    path('add-to-wishlist/<int:book_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:book_id>/', views.remove_from_wishlist_view, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
