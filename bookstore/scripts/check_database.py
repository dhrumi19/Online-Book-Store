import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

from bookstore.models import Category, Book

def check_database():
    print("🔍 Checking BookStore Database...")
    print("=" * 50)
    
    # Check categories
    categories = Category.objects.all()
    print(f"📚 Total Categories: {categories.count()}")
    for category in categories:
        print(f"  • {category.name}")
    
    print()
    
    # Check books
    books = Book.objects.all()
    print(f"📖 Total Books: {books.count()}")
    
    if books.exists():
        print("\n📋 All Books:")
        for book in books:
            print(f"  • {book.title} by {book.author} - ₹{book.price} (Stock: {book.stock})")
    else:
        print("❌ No books found in database!")
    
    # Check books with stock
    books_in_stock = Book.objects.filter(stock__gt=0)
    print(f"\n📦 Books in Stock: {books_in_stock.count()}")
    
    # Check by category
    print("\n📊 Books by Category:")
    for category in categories:
        book_count = Book.objects.filter(category=category, stock__gt=0).count()
        print(f"  • {category.name}: {book_count} books in stock")

if __name__ == "__main__":
    check_database()
