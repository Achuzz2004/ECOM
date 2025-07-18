==============================
🌀 Project Name - Ecom
==============================

A brief and clear description of your Django-based web application.

-------------------
📌 Features
-------------------
- User authentication (Login/Signup)
- Admin dashboard
- search Products
- Add products to cart
- Order products
- edit and view ordered products
- Responsive UI with Django templates

-------------------
🛠️ Tech Stack
-------------------
- Backend: Django (Python)
- Database: SQLite / PostgreSQL
- Frontend: HTML, CSS, Bootstrap 
- Other: Django Admin

-----------------------------
⚙️ Setup Instructions
-----------------------------

1. Clone the repository:
   git clone https://github.com/Achuzz2004/ECOM.git
   cd your-repo-name

2. Create and activate virtual environment:
   Windows:
     python -m venv venv
     venv\Scripts\activate
   macOS/Linux:
     python3 -m venv venv
     source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Start the development server:
   python manage.py runserver

   Open your browser at:
   http://127.0.0.1:8000/

-----------------------
🔐 Admin Login
-----------------------

Create admin user:
   python manage.py createsuperuser

Follow the prompt to set admin credentials.


-----------------------
📃 License
-----------------------
This project is open-source and available under the MIT License.
