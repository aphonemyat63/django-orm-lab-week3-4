
# DTI412 Lab 03-04

## Training Management System

This project demonstrates Django database models, migrations,
admin configuration, ORM queries, and database optimization.

## Models
- Department
- Employee
- Course
- TrainingRecord

## Features
- Department and employee management
- Training course enrollment
- Django admin interface
- Q and F expressions
- select_related() optimization
- prefetch_related() optimization

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   pip install -r requirements.txt

3. Run database migrations:
   python manage.py migrate

4. Create an admin user:
   python manage.py createsuperuser

5. Run the server:
   python manage.py runserver

6. Open:
   http://127.0.0.1:8000/admin/
