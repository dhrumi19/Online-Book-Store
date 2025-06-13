import random
import uuid
import json
from decimal import Decimal
from .models import Payment

def process_credit_card_payment(order, card_data):
    """Process a credit card payment"""
    success_rate = 95  # 95% success rate
    is_successful = random.randint(1, 100) <= success_rate
    
    payment_details = {
        'card_last4': card_data['card_number'][-4:],
        'card_expiry': card_data['expiry_date'],
        'card_type': get_card_type(card_data['card_number']),
        'card_name': card_data['card_name'],
    }
    
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='credit_card',
        status='completed' if is_successful else 'failed',
        payment_details=payment_details
    )
    
    if is_successful:
        order.status = 'confirmed'
        order.save()
        return payment, True, "Payment processed successfully"
    else:
        return payment, False, "Your card was declined. Please try another payment method."

def process_upi_payment(order, upi_data):
    """Process a UPI payment"""
    success_rate = 90  # 90% success rate
    is_successful = random.randint(1, 100) <= success_rate
    
    payment_details = {
        'upi_id': upi_data['upi_id'],
        'upi_provider': get_upi_provider(upi_data['upi_id']),
    }
    
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='upi',
        status='completed' if is_successful else 'failed',
        payment_details=payment_details
    )
    
    if is_successful:
        order.status = 'confirmed'
        order.save()
        return payment, True, "UPI payment processed successfully"
    else:
        return payment, False, "UPI payment failed. Please try again or use another payment method."

def process_net_banking_payment(order, bank_data):
    """Process a Net Banking payment"""
    success_rate = 88  # 88% success rate
    is_successful = random.randint(1, 100) <= success_rate
    
    payment_details = {
        'bank': bank_data['bank'],
        'bank_reference': f"NB-{uuid.uuid4().hex[:8].upper()}",
    }
    
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='net_banking',
        status='completed' if is_successful else 'failed',
        payment_details=payment_details
    )
    
    if is_successful:
        order.status = 'confirmed'
        order.save()
        return payment, True, "Net Banking payment processed successfully"
    else:
        return payment, False, "Net Banking payment failed. Please try again or use another payment method."

def process_wallet_payment(order, wallet_data):
    """Process a Digital Wallet payment"""
    success_rate = 92  # 92% success rate
    is_successful = random.randint(1, 100) <= success_rate
    
    payment_details = {
        'wallet': wallet_data['wallet'],
        'wallet_reference': f"WL-{uuid.uuid4().hex[:8].upper()}",
    }
    
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='wallet',
        status='completed' if is_successful else 'failed',
        payment_details=payment_details
    )
    
    if is_successful:
        order.status = 'confirmed'
        order.save()
        return payment, True, f"{wallet_data['wallet'].title()} payment processed successfully"
    else:
        return payment, False, f"{wallet_data['wallet'].title()} payment failed. Please try again or use another payment method."

def process_cod_payment(order):
    """Process a Cash on Delivery payment"""
    payment_details = {
        'cod_reference': f"COD-{uuid.uuid4().hex[:8].upper()}",
    }
    
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='cod',
        status='pending',  # COD payments are pending until delivery
        payment_details=payment_details
    )
    
    order.status = 'confirmed'
    order.save()
    
    return payment, True, "Cash on Delivery order placed successfully"

def get_card_type(card_number):
    """Determine the card type based on the card number"""
    card_number = card_number.replace(' ', '')
    
    if card_number.startswith('4'):
        return 'Visa'
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        return 'MasterCard'
    elif card_number.startswith(('34', '37')):
        return 'American Express'
    elif card_number.startswith('6'):
        return 'Discover'
    else:
        return 'Unknown'

def get_upi_provider(upi_id):
    """Determine the UPI provider based on the UPI ID"""
    if '@paytm' in upi_id:
        return 'Paytm'
    elif '@okicici' in upi_id:
        return 'ICICI Bank'
    elif '@okhdfcbank' in upi_id:
        return 'HDFC Bank'
    elif '@ybl' in upi_id:
        return 'PhonePe'
    elif '@upi' in upi_id:
        return 'BHIM'
    elif '@apl' in upi_id:
        return 'Amazon Pay'
    elif '@gpay' in upi_id:
        return 'Google Pay'
    else:
        return 'Other'
