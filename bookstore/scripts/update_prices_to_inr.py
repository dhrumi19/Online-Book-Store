import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

from bookstore.models import Book
from decimal import Decimal

def update_prices_to_inr():
    """Convert all book prices from USD to INR (approximate conversion)"""
    print("🔄 Converting book prices from USD to INR...")
    
    # Approximate conversion rate: 1 USD = 83 INR
    conversion_rate = 83
    
    books = Book.objects.all()
    updated_count = 0
    
    for book in books:
        # Convert price from USD to INR
        old_price = book.price
        new_price = old_price * conversion_rate
        
        # Round to nearest rupee
        book.price = round(new_price, 0)
        book.save()
        
        print(f"✅ {book.title}: ₹{old_price} → ₹{book.price}")
        updated_count += 1
    
    print(f"\n🎉 Successfully updated {updated_count} book prices to INR!")

if __name__ == "__main__":
    update_prices_to_inr()
