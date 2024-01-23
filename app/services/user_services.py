from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

import app
from flask import session, request
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.dbmodel import User, db, Online_users
import re
from app.services.general_services import hashText, checkHashedText


def create_logic():
    try:
        db.create_all()
        db.session.commit()
        return "table created successfully"
    except Exception as e:
        return "tables not created"


def is_valid_email(email):
    # Define a simple regular expression for email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)


def get_all_users():
    user_data = db.session.query(
        User.id, User.username, User.firstname, User.middlename, User.lastname, User.birthdate, User.email
    ).all()

    # Transforming query results into a list of dictionaries
    users = [
        {"id": u[0], "username": u[1], "firstname": u[2], "middlename": u[3], "lastname": u[4], "birthdate": u[5],
         "email": u[6]}
        for u in user_data
    ]

    return users


def get_online_users():
    online_users = db.session.query(
        Online_users.id,
        User.username,
        Online_users.ipaddress,
        Online_users.logindatetime
    ).join(User, Online_users.userId == User.id).all()

    return online_users


# todo create new user with hash
def create_new_user(username, firstname, middlename, lastname, birthdate, email, password):
    # Check if user already exists
    existing_user = db.session.query(User).filter(User.username == username).first()
    if existing_user:
        return None  # or you can raise an exception

    # Hash the password
    hashed_password = hashText(password)

    # Create new User instance
    new_user = User(
        username=username,
        firstname=firstname,
        middlename=middlename,
        lastname=lastname,
        birthdate=birthdate,
        email=email,
        password=hashed_password
    )

    # Add new user to the database session and commit
    db.session.add(new_user)
    try:
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return None


def user_login(email, password):
    # Query the database for the user
    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return False, "Username not found."

    # Check if the provided password matches the stored hash
    if not checkHashedText(user.password, password):
        return False, "Password is incorrect."

    # If the credentials are correct, set up the user session
    session['user_id'] = user.id
    session['username'] = user.username
    user_ip = request.remote_addr

    # Get the current date and time
    now = datetime.now(pytz.utc)  # Using UTC timezone, adjust as necessary

    # Add entry to online users table
    online_user_entry = Online_users(
        userId=user.id,
        ipaddress=user_ip,
        logindatetime=now
    )
    db.session.add(online_user_entry)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while updating online users: {e}")
        # You can decide how to handle this error. Maybe log the error or send a notification.

    return True, "Login successful."

def remove_online_user():
    user_id = session.get('user_id')
    if user_id:
        try:
            online_user = Online_users.query.filter_by(userId=user_id).first()
            if online_user:
                db.session.delete(online_user)
                db.session.commit()
                return True
        except Exception as e:
            db.session.rollback()
            print(f"Error during removing online user: {e}")
            return False
    return False
def remove_user_from_db(user_id):
    try:
        # Retrieve the user from the database
        existing_user = db.session.query(User).filter(User.id == user_id).first()

        # Check if the user exists
        if existing_user is None:
            return "User not found."

        # Delete the user
        db.session.delete(existing_user)

        # Commit the changes to the database
        db.session.commit()

        return "User successfully removed."
    except SQLAlchemyError as e:
        # Rollback in case of exception
        db.session.rollback()

        # Log the specific database error
        print(f"Database error occurred while removing user: {e}")

        return f"Error removing user: {e}"
    except Exception as e:
        # Handle non-database related exceptions
        print(f"An error occurred while removing user: {e}")

        return f"Error removing user: {e}"


def clear_session():
    session.clear()