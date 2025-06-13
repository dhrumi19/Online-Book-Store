import os
import sys
import django
from datetime import date
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

from bookstore.models import Category, Book

def create_categories():
    """Create book categories"""
    categories_data = [
        {
            'name': 'Fiction',
            'description': 'Novels, short stories, and other fictional works'
        },
        {
            'name': 'Non-Fiction',
            'description': 'Biographies, memoirs, and factual books'
        },
        {
            'name': 'Science & Technology',
            'description': 'Books about science, technology, and innovation'
        },
        {
            'name': 'Business',
            'description': 'Business, entrepreneurship, and management books'
        },
        {
            'name': 'Self-Help',
            'description': 'Personal development and self-improvement books'
        },
        {
            'name': 'History',
            'description': 'Historical events, periods, and figures'
        },
        {
            'name': 'Philosophy',
            'description': 'Philosophical thoughts and theories'
        },
        {
            'name': 'Romance',
            'description': 'Love stories and romantic novels'
        },
        {
            'name': 'Mystery & Thriller',
            'description': 'Suspenseful and thrilling stories'
        },
        {
            'name': 'Children & Young Adult',
            'description': 'Books for children and young adults'
        }
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"📚 Category already exists: {category.name}")

def create_books():
    """Create 30 books across different categories"""
    
    # Get categories
    try:
        fiction = Category.objects.get(name='Fiction')
        non_fiction = Category.objects.get(name='Non-Fiction')
        science = Category.objects.get(name='Science & Technology')
        business = Category.objects.get(name='Business')
        self_help = Category.objects.get(name='Self-Help')
        history = Category.objects.get(name='History')
        philosophy = Category.objects.get(name='Philosophy')
        romance = Category.objects.get(name='Romance')
        mystery = Category.objects.get(name='Mystery & Thriller')
        children = Category.objects.get(name='Children & Young Adult')
    except Category.DoesNotExist as e:
        print(f"❌ Error: Category not found - {e}")
        return
    
    books_data = [
        # Fiction Books (8 books)
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'category': fiction,
            'description': 'A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream.',
            'price': 12.99,
            'stock': 25,
            'isbn': '9780743273565',
            'publication_date': date(1925, 4, 10)
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'category': fiction,
            'description': 'A gripping tale of racial injustice and childhood innocence in the American South.',
            'price': 14.99,
            'stock': 30,
            'isbn': '9780061120084',
            'publication_date': date(1960, 7, 11)
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'category': fiction,
            'description': 'A dystopian social science fiction novel about totalitarian control and surveillance.',
            'price': 13.99,
            'stock': 20,
            'isbn': '9780451524935',
            'publication_date': date(1949, 6, 8)
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'category': fiction,
            'description': 'A romantic novel that critiques the British landed gentry at the end of the 18th century.',
            'price': 11.99,
            'stock': 22,
            'isbn': '9780141439518',
            'publication_date': date(1813, 1, 28)
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'category': fiction,
            'description': 'A controversial novel about teenage rebellion and alienation.',
            'price': 13.99,
            'stock': 26,
            'isbn': '9780316769174',
            'publication_date': date(1951, 7, 16)
        },
        {
            'title': 'Lord of the Flies',
            'author': 'William Golding',
            'category': fiction,
            'description': 'A group of British boys stranded on an uninhabited island.',
            'price': 12.99,
            'stock': 24,
            'isbn': '9780571056866',
            'publication_date': date(1954, 9, 17)
        },
        {
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'category': fiction,
            'description': 'A philosophical story about following your dreams.',
            'price': 14.99,
            'stock': 38,
            'isbn': '9780061122415',
            'publication_date': date(1988, 1, 1)
        },
        {
            'title': 'Harry Potter and the Sorcerer\'s Stone',
            'author': 'J.K. Rowling',
            'category': fiction,
            'description': 'The first book in the magical Harry Potter series.',
            'price': 16.99,
            'stock': 45,
            'isbn': '9780439708180',
            'publication_date': date(1997, 6, 26)
        },
        
        # Romance Books (3 books)
        {
            'title': 'The Notebook',
            'author': 'Nicholas Sparks',
            'category': romance,
            'description': 'A touching love story that spans decades, showing the enduring power of true love.',
            'price': 15.99,
            'stock': 18,
            'isbn': '9780446605236',
            'publication_date': date(1996, 10, 1)
        },
        {
            'title': 'Me Before You',
            'author': 'Jojo Moyes',
            'category': romance,
            'description': 'A heart-wrenching story about love, loss, and the choices we make.',
            'price': 16.99,
            'stock': 15,
            'isbn': '9780143124542',
            'publication_date': date(2012, 1, 5)
        },
        {
            'title': 'The Fault in Our Stars',
            'author': 'John Green',
            'category': romance,
            'description': 'A beautiful love story between two teenagers with cancer.',
            'price': 14.99,
            'stock': 32,
            'isbn': '9780525478812',
            'publication_date': date(2012, 1, 10)
        },
        
        # Non-Fiction Books (3 books)
        {
            'title': 'Sapiens',
            'author': 'Yuval Noah Harari',
            'category': non_fiction,
            'description': 'A brief history of humankind, exploring how Homo sapiens came to dominate the world.',
            'price': 18.99,
            'stock': 35,
            'isbn': '9780062316097',
            'publication_date': date(2014, 9, 4)
        },
        {
            'title': 'Educated',
            'author': 'Tara Westover',
            'category': non_fiction,
            'description': 'A memoir about education, family, and the struggle between loyalty and independence.',
            'price': 17.99,
            'stock': 28,
            'isbn': '9780399590504',
            'publication_date': date(2018, 2, 20)
        },
        {
            'title': 'Becoming',
            'author': 'Michelle Obama',
            'category': non_fiction,
            'description': 'An intimate memoir by the former First Lady of the United States.',
            'price': 19.99,
            'stock': 40,
            'isbn': '9781524763138',
            'publication_date': date(2018, 11, 13)
        },
        
        # Science & Technology Books (3 books)
        {
            'title': 'A Brief History of Time',
            'author': 'Stephen Hawking',
            'category': science,
            'description': 'A landmark volume in science writing that explores the nature of time and the universe.',
            'price': 16.99,
            'stock': 25,
            'isbn': '9780553380163',
            'publication_date': date(1988, 4, 1)
        },
        {
            'title': 'The Innovators',
            'author': 'Walter Isaacson',
            'category': science,
            'description': 'The story of the people who created the computer and the Internet.',
            'price': 20.99,
            'stock': 20,
            'isbn': '9781476708690',
            'publication_date': date(2014, 10, 7)
        },
        {
            'title': 'Cosmos',
            'author': 'Carl Sagan',
            'category': science,
            'description': 'A journey through the universe, exploring astronomy, evolution, and the search for life.',
            'price': 15.99,
            'stock': 30,
            'isbn': '9780345331359',
            'publication_date': date(1980, 9, 28)
        },
        
        # Business Books (3 books)
        {
            'title': 'Think and Grow Rich',
            'author': 'Napoleon Hill',
            'category': business,
            'description': 'A classic guide to success and wealth-building through positive thinking.',
            'price': 14.99,
            'stock': 32,
            'isbn': '9781585424337',
            'publication_date': date(1937, 8, 1)
        },
        {
            'title': 'Good to Great',
            'author': 'Jim Collins',
            'category': business,
            'description': 'Why some companies make the leap to greatness while others don\'t.',
            'price': 18.99,
            'stock': 24,
            'isbn': '9780066620992',
            'publication_date': date(2001, 10, 16)
        },
        {
            'title': 'Rich Dad Poor Dad',
            'author': 'Robert T. Kiyosaki',
            'category': business,
            'description': 'What the rich teach their kids about money that the poor and middle class do not.',
            'price': 16.99,
            'stock': 42,
            'isbn': '9781612680194',
            'publication_date': date(1997, 4, 1)
        },
        
        # Self-Help Books (3 books)
        {
            'title': 'The 7 Habits of Highly Effective People',
            'author': 'Stephen R. Covey',
            'category': self_help,
            'description': 'A powerful lesson in personal change and effectiveness.',
            'price': 16.99,
            'stock': 35,
            'isbn': '9781982137274',
            'publication_date': date(1989, 8, 15)
        },
        {
            'title': 'How to Win Friends and Influence People',
            'author': 'Dale Carnegie',
            'category': self_help,
            'description': 'Timeless advice on building relationships and influencing others.',
            'price': 15.99,
            'stock': 40,
            'isbn': '9780671027032',
            'publication_date': date(1936, 10, 1)
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'category': self_help,
            'description': 'An easy and proven way to build good habits and break bad ones.',
            'price': 18.99,
            'stock': 45,
            'isbn': '9780735211292',
            'publication_date': date(2018, 10, 16)
        },
        
        # History Books (3 books)
        {
            'title': 'The Guns of August',
            'author': 'Barbara Tuchman',
            'category': history,
            'description': 'A detailed account of the first month of World War I.',
            'price': 17.99,
            'stock': 20,
            'isbn': '9780345476098',
            'publication_date': date(1962, 1, 1)
        },
        {
            'title': 'A People\'s History of the United States',
            'author': 'Howard Zinn',
            'category': history,
            'description': 'American history from the perspective of ordinary people.',
            'price': 19.99,
            'stock': 25,
            'isbn': '9780062397348',
            'publication_date': date(1980, 1, 1)
        },
        {
            'title': 'The Diary of a Young Girl',
            'author': 'Anne Frank',
            'category': history,
            'description': 'The powerful diary of a Jewish girl hiding during the Holocaust.',
            'price': 13.99,
            'stock': 30,
            'isbn': '9780553296983',
            'publication_date': date(1947, 6, 25)
        },
        
        # Philosophy Books (2 books)
        {
            'title': 'Meditations',
            'author': 'Marcus Aurelius',
            'category': philosophy,
            'description': 'Personal writings by the Roman Emperor on Stoic philosophy.',
            'price': 12.99,
            'stock': 22,
            'isbn': '9780486298238',
            'publication_date': date(180, 1, 1)
        },
        {
            'title': 'Man\'s Search for Meaning',
            'author': 'Viktor E. Frankl',
            'category': philosophy,
            'description': 'A Holocaust survivor\'s reflections on finding purpose in suffering.',
            'price': 15.99,
            'stock': 35,
            'isbn': '9780807014295',
            'publication_date': date(1946, 1, 1)
        },
        
        # Mystery & Thriller Books (2 books)
        {
            'title': 'Gone Girl',
            'author': 'Gillian Flynn',
            'category': mystery,
            'description': 'A psychological thriller about a marriage gone terribly wrong.',
            'price': 16.99,
            'stock': 28,
            'isbn': '9780307588364',
            'publication_date': date(2012, 6, 5)
        },
        {
            'title': 'The Girl with the Dragon Tattoo',
            'author': 'Stieg Larsson',
            'category': mystery,
            'description': 'A gripping mystery involving murder, family secrets, and corruption.',
            'price': 15.99,
            'stock': 24,
            'isbn': '9780307454546',
            'publication_date': date(2005, 8, 1)
        },
        
        # Children & Young Adult Books (2 books)
        {
            'title': 'The Hunger Games',
            'author': 'Suzanne Collins',
            'category': children,
            'description': 'A dystopian novel about a televised fight to the death.',
            'price': 14.99,
            'stock': 35,
            'isbn': '9780439023528',
            'publication_date': date(2008, 9, 14)
        },
        {
            'title': 'Wonder',
            'author': 'R.J. Palacio',
            'category': children,
            'description': 'A story about a boy with facial differences starting school.',
            'price': 13.99,
            'stock': 40,
            'isbn': '9780375869020',
            'publication_date': date(2012, 2, 14)
        }
    ]
    
    created_count = 0
    for book_data in books_data:
        try:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                print(f"✅ Created book: {book.title} by {book.author} - ₹{book.price}")
                created_count += 1
            else:
                print(f"📖 Book already exists: {book.title}")
        except Exception as e:
            print(f"❌ Error creating book {book_data['title']}: {e}")
    
    print(f"\n🎉 Successfully created {created_count} new books!")

def main():
    print("🚀 Setting up BookStore database...")
    print("=" * 50)
    
    print("\n📚 Creating categories...")
    create_categories()
    
    print(f"\n📖 Creating books...")
    create_books()
    
    print("\n" + "=" * 50)
    print("✅ Database setup complete!")
    print(f"📊 Total categories: {Category.objects.count()}")
    print(f"📚 Total books: {Book.objects.count()}")
    print(f"📦 Books in stock: {Book.objects.filter(stock__gt=0).count()}")
    
    # Show books by category
    print("\n📋 Books by Category:")
    for category in Category.objects.all():
        book_count = Book.objects.filter(category=category).count()
        print(f"  • {category.name}: {book_count} books")

if __name__ == "__main__":
    main()
