from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Book, Category, Cart, Order, OrderItem, Wishlist
from .serializers import (
    BookSerializer, CategorySerializer, CartSerializer, 
    OrderSerializer, WishlistSerializer
)

@api_view(['GET'])
def api_books_list(request):
    """API endpoint to get all books"""
    books = Book.objects.filter(stock__gt=0)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        books = books.filter(
            Q(title__icontains=search) | 
            Q(author__icontains=search) |
            Q(description__icontains=search)
        )
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_book_detail(request, book_id):
    """API endpoint to get book details"""
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])
def api_categories_list(request):
    """API endpoint to get all categories"""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_cart(request):
    """API endpoint for cart operations"""
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        total = sum(item.total_price for item in cart_items)
        return Response({
            'cart_items': serializer.data,
            'total': total
        })
    
    elif request.method == 'POST':
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        book = get_object_or_404(Book, id=book_id)
        
        if not book.is_available:
            return Response({'error': 'Book is out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_cart_item(request, cart_id):
    """API endpoint to update or remove cart item"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'PUT':
        quantity = request.data.get('quantity')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            serializer = CartSerializer(cart_item)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_checkout(request):
    """API endpoint for checkout"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    total = sum(item.total_price for item in cart_items)
    shipping_address = request.data.get('shipping_address', '')
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        shipping_address=shipping_address
    )
    
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=cart_item.book,
            quantity=cart_item.quantity,
            price=cart_item.book.price
        )
        
        # Update stock
        book = cart_item.book
        book.stock -= cart_item.quantity
        book.save()
    
    # Clear cart
    cart_items.delete()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_orders(request):
    """API endpoint to get user orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_order_detail(request, order_id):
    """API endpoint to get order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_wishlist(request):
    """API endpoint for wishlist operations"""
    if request.method == 'GET':
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            book=book
        )
        
        if created:
            serializer = WishlistSerializer(wishlist_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Book already in wishlist'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_wishlist_remove(request, book_id):
    """API endpoint to remove item from wishlist"""
    book = get_object_or_404(Book, id=book_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, book=book)
    wishlist_item.delete()
    return Response({'message': 'Item removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
