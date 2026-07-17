# Fashion shop website prototype (fullstack)

Fashion store website prototype developed for my freelance work assignment. Due to a shrinking deadline, the entire application was designed (strong word after seeing
my frontend but aight) and implemented in just four days.

Website uses HTML, CSS and JavaScript for the frontend and backend is powered on Python FastAPI. For SQL and SQL operations it uses SQLAlchemy and SQLAlchemy.orm to 
work with database, allowing it directly from the code without writing raw SQL queries.

The application (if you can call it that) supports searching through the catalogue via search engine, category filtering and a shopping cart.
A catalogue and shopping cart functions (i.e product data) is retrieved from the backend to provide code safety and improve overall project logic.

For me, this is a huge jump from konwing basic JS from college to learning and instantly implementing new functions and JS opportunities in real projects, as well as getting experience in working 
with SQL commands in Python.

## Features
- Dynamic product catalogue
- Product search
- Category filtering
- Size selection
- Automate price calcultaion
- Shopping cart functionality
- Rest API communication between frontend and backend
- CRUD operations for products and shopping cart items
- Responsive grid layout
- SQLite intergation w/ SQLAlchemy
- Data fetching and storage with SQL database

## Install
1. **Clone the repository.** Use your cmd and perform next operation: 

  ```bash
  git clone https://github.com/rrusls/fashion-shop-fullstack.git
  cd fashion-shop-fullstack
  ```
2. **Create and activate a virtual environment.** This keeps project dependencies isolated from your global Python install.
   ```bash
     python -m venv venv
   ```
   Then activate it:
   ```bash
      # Windows
      venv/Scripts/activate
      # macOS/Linux
      source venv/bin/activate
   ```
   You will see `(venv)` in terminal prompt after it's successful activation.

4. **Install Python dependencies.** Make sure your Python version is fresh and pip works normally.

  ```bash
     pip install -r requirements.txt
  ```
4. **Start the FastAPI server**. Start the server to connect frontend and backend.
   
  ```bash
  uvicorn main:app --reload
  ```
  The **backend** will be available at:

  ```
  http://127.0.0.1:8000
  ```
 5. **Open `fashion-shop.html` in your browser.** See fashion shop on your screen.
  The application will automatically connect to the running backend and use the included SQLite database (`mara.db`).
  
## Future improvements 
  - Improve overall look of page via CSS
  - Add hovers and animations
  - Build an account system (user authentication)
  - Add user's wishlist
  - Payment system simulation (or not simulation!)
  - Reviews on product
  - Improve quality of JS scripts

## Important
This project is my latest achievement and will change a lot in the near future. I will try
to show my growing everytime I commit some changes. This way my progress in web-development would be obvious and easy to track.
Thanks for reading 
