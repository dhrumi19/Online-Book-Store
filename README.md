# Online-Book-Store
📚 Online Bookstore — Full Stack Web Application (Django) This project is a complete online bookstore platform built using the Django web framework, incorporating both frontend and backend components. It allows users to browse books, add them to the cart, place orders, and track deliveries, while admins can manage inventory and process orders. 

🔍 Key Features
🔐 User Authentication: Signup, login, logout with session management.
🛍️ Book Browsing: View books by categories, search by title/author, and see detailed book pages.
🛒 Cart System: Add/remove books from cart, update quantity, and view cart total.
💳 Checkout & Payments: Choose from UPI, Credit Card, or Cash on Delivery (COD) during checkout.
🚚 Order Tracking: Users can track the real-time status of their placed orders.
🛠️ Admin Panel: Add/edit/delete books, manage orders and customers from a Django admin interface.
🎨 UI/UX: Clean Bootstrap-based responsive interface for a better user experience.

🛠 Tech Stack
| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| Django                    | Backend framework (Python)      |
| SQLite                    | Development database            |
| HTML/CSS                  | Frontend structure & styling    |
| Bootstrap                 | Responsive UI design            |
| JavaScript                | Cart interactions, order status |
| Razorpay/Paytm (optional) | Payment gateway integration     |

📂 Project Structure (Simplified)
online_bookstore/
├── bookstore/         # Django app for books, cart, orders
├── users/             # Handles login, signup, user profile
├── templates/         # HTML templates
├── static/            # CSS, JS, Images
├── media/             # Book images, uploads
├── db.sqlite3         # Database
├── manage.py

📚 Learning Outcomes
Built a full-stack application with Django.
Gained experience in session management, model relationships, and admin interfaces.
Learned to integrate frontend interactivity and payment options.
Applied software engineering principles like modularity, testing, and deployment.

📌 Future Improvements
Two Factor Authentication when Customer Use to Signup they use to Email notification For OTP
Email notifications for order confirmation.
Product ratings and reviews.
Discount coupons and offer banners.
Advanced filtering and sorting by category/price/author.
