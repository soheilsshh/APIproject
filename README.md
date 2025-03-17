# Store Shop - E-Commerce API

## Description  

**Store Shop** is an e-commerce platform developed using API technology. This project provides a basic shopping site functionality, allowing users to create and manage their profiles, log in and out, and perform all necessary actions related to product management.  

The core features include:  
- User authentication (sign up, login, and logout).  
- User profile management.  
- Product creation, update, and deletion.  
- Exposing product data via API endpoints.  
- A RESTful API designed to handle essential e-commerce tasks.  

This project can be extended with additional features such as payment integration, cart management, product reviews, and more. It is designed to be a foundation for a fully functional shopping website.

## Features  

- ✅ **User Authentication:** Register, log in, and log out.  
- ✅ **Profile Management:** Users can manage their profiles.  
- ✅ **Product Management:** Create, update, and delete products.  
- ✅ **API Endpoints:** Expose product data and user profile information through API.  
- ✅ **CRUD Operations:** Full CRUD (Create, Read, Update, Delete) functionality for products.  

## Installation  

### 1. Clone the Repository  
Start by cloning the repository:  
```bash
git clone https://github.com/soheilsshh/APIproject.git
cd APIproject
```
### 2. Set Up Virtual Environment with Pipenv
Ensure you have pipenv installed:

```bash
pip install pipenv
```
Then, create and activate the virtual environment:

```bash
pipenv install
pipenv shell
```
### 3. Install Dependencies
Install all the required dependencies by running:

```bash
pipenv install -r requirements.txt
```
### 4. Apply Migrations
Before starting the project, run the database migrations:

```bash
python manage.py migrate
```
### 5. Create a Superuser (Optional)
To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```
Fill in the necessary details when prompted.

### 6. Run the Development Server
Start the development server:

```bash
python manage.py runserver
```
The project will be available at http://127.0.0.1:8000/.

## Usage
Access the API at http://127.0.0.1:8000/store/ for all the product and profile-related actions.
Use tools like Postman or Insomnia to test the API endpoints (e.g., POST requests for creating products, GET requests for retrieving products).
Register a new user, log in, and perform actions such as creating or managing products.
Use the provided endpoints to interact with the database.
## Technologies Used
Django – Backend framework for developing the API.
Django REST Framework – For creating RESTful APIs.
Python – Core programming language.
SQLite (default) – Database (can be replaced with PostgreSQL or MySQL).
##Future Improvements
🔹 Payment Integration: Implement a payment gateway to handle transactions.
🔹 Cart Management: Add functionality for adding products to a shopping cart.
🔹 User Reviews: Allow users to leave product reviews and ratings.
🔹 Search Functionality: Add advanced search filters (by category, price, etc.).
