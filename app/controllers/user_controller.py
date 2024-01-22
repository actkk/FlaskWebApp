import json
from app.models.dbmodel import InsertTable,db
from app.services.user_services import create_logic

def index():
    return {'status': 'OK',
            'localhost:5000/users':'Created tables '
            }
def create():
    create_logic()














# # app/controllers/user_controller.py
# import re
# from flask import jsonify, request, render_template, redirect, url_for
# from app import app, db
# from app.models import User
# def is_valid_email(email):
#     # Define a simple regular expression for email validation
#     email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     return re.match(email_regex, email)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error_message = None
#
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         # Validate if the entered value is a valid email address
#         if not is_valid_email(email):
#             error_message = "Invalid email format"
#             return render_template('login.html', error=error_message)
#
#         user = User.query.filter_by(email=email).first()
#
#         if user and user.verify_password(password):
#             # Authentication successful
#             return render_template('user_list.html', email=email)
#         else:
#             # Authentication failed
#             error_message = "Invalid email or password"
#
#     return render_template('login.html', error=error_message)
#
#
#
# @app.route('/user/create', methods=['GET', 'POST'])
# def create_user():
#     error_message = None
#
#     if request.method == 'POST':
#         username = request.form['username']
#         firstname = request.form['firstname']
#         middlename = request.form['middlename']
#         lastname = request.form['lastname']
#         birthdate = request.form['birthdate']
#         email = request.form['email']
#         password = request.form['password']
#
#         # Validate if the entered value is a valid email address
#         if not is_valid_email(email):
#             error_message = "Invalid email format"
#             return render_template('create_user.html', error=error_message)
#
#         # Check if the email already exists in the database
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             error_message = "Email is already registered"
#             return render_template('create_user.html', error=error_message)
#
#         # Create a new user
#         new_user = User(
#             username=username,
#             firstname=firstname,
#             middlename=middlename,
#             lastname=lastname,
#             birthdate=birthdate,
#             email=email,
#             password=password  # In a real application, you should hash the password
#         )
#
#         # Add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#
#         return redirect(url_for('user_list'))  # Redirect to user list page after successful creation
#
#     return render_template('create_user.html', error=error_message)
# @app.route('/user/list', methods=['GET'])
# def user_list():
#     users = User.query.all()
#     return render_template('user_list.html', users=users)
#
# # Implement other CRUD operations here
