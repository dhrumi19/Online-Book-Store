from django.contrib import admin
from .models import Category, Book, Cart, Order, OrderItem, Wishlist, Payment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['price', 'stock']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']
    list_editable = ['status']
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['order__id', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']
