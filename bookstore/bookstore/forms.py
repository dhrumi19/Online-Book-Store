from django import forms
from .models import Payment

class ShippingAddressForm(forms.Form):
    full_name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        }),
        label='Full Name'
    )
    phone = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 9876543210'
        }),
        label='Phone Number'
    )
    address_line1 = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'House/Flat No., Building Name'
        }),
        label='Address Line 1'
    )
    address_line2 = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street, Area, Landmark (Optional)'
        }),
        label='Address Line 2'
    )
    city = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }),
        label='City'
    )
    state = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State'
        }),
        label='State'
    )
    pincode = forms.CharField(
        max_length=6, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '400001'
        }),
        label='PIN Code'
    )

class PaymentMethodForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Digital Wallet (Paytm, PhonePe, etc.)'),
        ('cod', 'Cash on Delivery'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Payment Method'
    )

class CreditCardPaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456'
        }),
        label='Card Number'
    )
    expiry_date = forms.CharField(
        max_length=5, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY'
        }),
        label='Expiry Date'
    )
    cvv = forms.CharField(
        max_length=4, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123'
        }),
        label='CVV'
    )
    card_name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on Card'
        }),
        label='Cardholder Name'
    )

class UPIPaymentForm(forms.Form):
    upi_id = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'yourname@paytm'
        }),
        label='UPI ID'
    )

class NetBankingForm(forms.Form):
    BANK_CHOICES = [
        ('sbi', 'State Bank of India'),
        ('hdfc', 'HDFC Bank'),
        ('icici', 'ICICI Bank'),
        ('axis', 'Axis Bank'),
        ('kotak', 'Kotak Mahindra Bank'),
        ('pnb', 'Punjab National Bank'),
        ('bob', 'Bank of Baroda'),
        ('canara', 'Canara Bank'),
    ]
    
    bank = forms.ChoiceField(
        choices=BANK_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Your Bank'
    )

class WalletPaymentForm(forms.Form):
    WALLET_CHOICES = [
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('googlepay', 'Google Pay'),
        ('amazonpay', 'Amazon Pay'),
        ('mobikwik', 'MobiKwik'),
    ]
    
    wallet = forms.ChoiceField(
        choices=WALLET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Wallet'
    )