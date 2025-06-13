from django.urls import path
from . import api_views

urlpatterns = [
    path('books/', api_views.api_books_list, name='api_books_list'),
    path('books/<int:book_id>/', api_views.api_book_detail, name='api_book_detail'),
    path('categories/', api_views.api_categories_list, name='api_categories_list'),
    path('cart/', api_views.api_cart, name='api_cart'),
    path('cart/<int:cart_id>/', api_views.api_cart_item, name='api_cart_item'),
    path('checkout/', api_views.api_checkout, name='api_checkout'),
    path('orders/', api_views.api_orders, name='api_orders'),
    path('orders/<int:order_id>/', api_views.api_order_detail, name='api_order_detail'),
    path('wishlist/', api_views.api_wishlist, name='api_wishlist'),
    path('wishlist/remove/<int:book_id>/', api_views.api_wishlist_remove, name='api_wishlist_remove'),
]
