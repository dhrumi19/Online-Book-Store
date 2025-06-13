from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from .models import Book, Category, Cart, Order, OrderItem, Wishlist, Payment
from .forms import ShippingAddressForm, PaymentMethodForm, CreditCardPaymentForm, UPIPaymentForm, NetBankingForm, WalletPaymentForm
from .payment_utils import process_credit_card_payment, process_upi_payment, process_cod_payment, process_net_banking_payment, process_wallet_payment

@login_required
def home_view(request):
    categories = Category.objects.all()
    featured_books = Book.objects.all()[:8]
    
    context = {
        'categories': categories,
        'featured_books': featured_books,
    }
    return render(request, 'bookstore/home.html', context)

@login_required
def book_list_view(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'bookstore/book_list.html', context)

@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    related_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)[:4]
    
    # Check if book is in wishlist
    in_wishlist = Wishlist.objects.filter(user=request.user, book=book).exists()
    
    context = {
        'book': book,
        'related_books': related_books,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'bookstore/book_detail.html', context)

@login_required
def add_to_cart_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.is_available:
        messages.error(request, 'This book is out of stock.')
        return redirect('bookstore:book_detail', book_id=book.id)
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        if cart_item.quantity < book.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Added another copy of "{book.title}" to cart.')
        else:
            messages.warning(request, 'Cannot add more items. Stock limit reached.')
    else:
        messages.success(request, f'"{book.title}" added to cart.')
    
    return redirect('bookstore:cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)
    
    # Calculate shipping
    shipping_cost = Decimal('0.00') if subtotal >= 999 else Decimal('50.00')
    total = subtotal + shipping_cost
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
        'free_shipping_threshold': 999,
    }
    return render(request, 'bookstore/cart.html', context)

@login_required
def update_cart_view(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0 and quantity <= cart_item.book.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            messages.error(request, 'Invalid quantity.')
    
    return redirect('bookstore:cart')

@login_required
def remove_from_cart_view(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()
    messages.success(request, f'"{book_title}" removed from cart.')
    return redirect('bookstore:cart')

@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('bookstore:cart')
    
    subtotal = sum(item.total_price for item in cart_items)
    shipping_cost = Decimal('0.00') if subtotal >= 999 else Decimal('50.00')
    total = subtotal + shipping_cost
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Format shipping address
            shipping_address = f"{form.cleaned_data['full_name']}\n"
            shipping_address += f"Phone: {form.cleaned_data['phone']}\n"
            shipping_address += f"{form.cleaned_data['address_line1']}\n"
            if form.cleaned_data['address_line2']:
                shipping_address += f"{form.cleaned_data['address_line2']}\n"
            shipping_address += f"{form.cleaned_data['city']}, {form.cleaned_data['state']} - {form.cleaned_data['pincode']}"
            
            # Create order with transaction to ensure data integrity
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
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
                
                # Don't update stock or clear cart yet - do it after payment
            
            # Redirect to payment page
            return redirect('bookstore:payment', order_id=order.id)
        else:
            messages.error(request, 'Please fill in all required fields correctly.')
    else:
        form = ShippingAddressForm()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
        'form': form,
        'free_shipping_threshold': 999,
    }
    return render(request, 'bookstore/checkout.html', context)

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if Payment.objects.filter(order=order, status='completed').exists():
        messages.info(request, 'This order has already been paid for.')
        return redirect('bookstore:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'credit_card':
            card_data = {
                'card_number': request.POST.get('card_number', '').replace(' ', ''),
                'expiry_date': request.POST.get('expiry_date', ''),
                'cvv': request.POST.get('cvv', ''),
                'card_name': request.POST.get('card_name', ''),
            }
            
            payment, success, message = process_credit_card_payment(order, card_data)
            
            if success:
                # Update stock and clear cart after successful payment
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    book = cart_item.book
                    book.stock -= cart_item.quantity
                    book.save()
                cart_items.delete()
                
                messages.success(request, message)
                return redirect('bookstore:payment_success', payment_id=payment.id)
            else:
                messages.error(request, message)
                return redirect('bookstore:payment_failed', order_id=order.id)
                
        elif payment_method == 'upi':
            upi_data = {
                'upi_id': request.POST.get('upi_id', ''),
            }
            
            payment, success, message = process_upi_payment(order, upi_data)
            
            if success:
                # Update stock and clear cart after successful payment
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    book = cart_item.book
                    book.stock -= cart_item.quantity
                    book.save()
                cart_items.delete()
                
                messages.success(request, message)
                return redirect('bookstore:payment_success', payment_id=payment.id)
            else:
                messages.error(request, message)
                return redirect('bookstore:payment_failed', order_id=order.id)
                
        elif payment_method == 'net_banking':
            bank_data = {
                'bank': request.POST.get('bank', ''),
            }
            
            payment, success, message = process_net_banking_payment(order, bank_data)
            
            if success:
                # Update stock and clear cart after successful payment
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    book = cart_item.book
                    book.stock -= cart_item.quantity
                    book.save()
                cart_items.delete()
                
                messages.success(request, message)
                return redirect('bookstore:payment_success', payment_id=payment.id)
            else:
                messages.error(request, message)
                return redirect('bookstore:payment_failed', order_id=order.id)
                
        elif payment_method == 'wallet':
            wallet_data = {
                'wallet': request.POST.get('wallet', ''),
            }
            
            payment, success, message = process_wallet_payment(order, wallet_data)
            
            if success:
                # Update stock and clear cart after successful payment
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    book = cart_item.book
                    book.stock -= cart_item.quantity
                    book.save()
                cart_items.delete()
                
                messages.success(request, message)
                return redirect('bookstore:payment_success', payment_id=payment.id)
            else:
                messages.error(request, message)
                return redirect('bookstore:payment_failed', order_id=order.id)
                
        elif payment_method == 'cod':
            payment, success, message = process_cod_payment(order)
            
            if success:
                # Update stock and clear cart after successful payment
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    book = cart_item.book
                    book.stock -= cart_item.quantity
                    book.save()
                cart_items.delete()
                
                messages.success(request, message)
                return redirect('bookstore:payment_success', payment_id=payment.id)
            else:
                messages.error(request, message)
                return redirect('bookstore:payment_failed', order_id=order.id)
        
        else:
            messages.error(request, 'Invalid payment method selected.')
    
    context = {
        'order': order,
    }
    return render(request, 'bookstore/payment.html', context)

@login_required
def payment_success_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__user=request.user)
    
    context = {
        'payment': payment,
    }
    return render(request, 'bookstore/payment_success.html', context)

@login_required
def payment_failed_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    error_message = request.GET.get('error', 'An unknown error occurred during payment processing.')
    
    context = {
        'order': order,
        'error_message': error_message,
    }
    return render(request, 'bookstore/payment_failed.html', context)

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'bookstore/order_detail.html', context)

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'bookstore/order_history.html', context)

@login_required
def track_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'bookstore/track_order.html', context)

@login_required
def cancel_order_view(request, order_id):
    """Cancel an order if it's eligible for cancellation"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if not order.can_be_cancelled:
        messages.error(request, 'This order cannot be cancelled as it has already been shipped or delivered.')
        return redirect('bookstore:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        # Cancel the order
        order.status = 'cancelled'
        order.save()
        
        # Restore stock for cancelled orders
        for item in order.items.all():
            book = item.book
            book.stock += item.quantity
            book.save()
        
        # Handle payment refund if payment was completed
        completed_payments = Payment.objects.filter(order=order, status='completed')
        for payment in completed_payments:
            payment.status = 'refunded'
            payment.save()
        
        messages.success(request, f'Order #{order.id} has been cancelled successfully. Stock has been restored and refund will be processed if applicable.')
        return redirect('bookstore:order_history')
    
    context = {
        'order': order,
    }
    return render(request, 'bookstore/cancel_order.html', context)

@login_required
def add_to_wishlist_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    if created:
        messages.success(request, f'"{book.title}" added to wishlist.')
    else:
        messages.info(request, f'"{book.title}" is already in your wishlist.')
    
    return redirect('bookstore:book_detail', book_id=book.id)

@login_required
def remove_from_wishlist_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, book=book)
    wishlist_item.delete()
    messages.success(request, f'"{book.title}" removed from wishlist.')
    return redirect('bookstore:wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request, 'bookstore/wishlist.html', context)
