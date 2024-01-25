from flask import session, request
from datetime import datetime
import pytz
from app.models.dbmodel import User, db, Online_users
from app.services.general_services import hash_text, check_hashed_text, is_valid_password
from app.log.logger import log


def create_logic():
    try:
        db.create_all()
        db.session.commit()
        log("Successfully db created")
        return "table created successfully"

    except Exception as e:
        return "tables not created"


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
    log("Successfully fetched all users")
    return users


def get_online_users():
    online_users = db.session.query(
        Online_users.id,
        User.username,
        Online_users.ipaddress,
        Online_users.logindatetime
    ).join(User, Online_users.userId == User.id).all()
    log("Successfully fetched online users")

    return online_users


def create_new_user(username, firstname, middlename, lastname, birthdate, email, password):

    existing_user = db.session.query(User).filter(User.username == username).first()
    if existing_user:
        return None

    hashed_password = hash_text(password)

    new_user = User(
        username=username,
        firstname=firstname,
        middlename=middlename,
        lastname=lastname,
        birthdate=birthdate,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        message = f"New user {new_user.id} added successfully"
        log(message)
        return new_user
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        message = f"An error occurred: {e} adding new user"
        log(message)
        return None


def user_login(email, password):
    # Query the database for the user
    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return False, "Username not found."

    if not check_hashed_text(user.password, password):
        return False, "Password is incorrect."

    # If the credentials are correct, set up the user session
    session['user_id'] = user.id
    session['username'] = user.username
    user_ip = request.remote_addr

    now = datetime.now(pytz.utc)

    online_user_entry = Online_users(
        userId=user.id,
        ipaddress=user_ip,
        logindatetime=now
    )
    db.session.add(online_user_entry)
    try:
        db.session.commit()
        message = f"User {user.id}  logged in"
        log(message)
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while updating online users: {e}")

    return True, "Login successful."


def check_username_exists(username):
    user = db.session.query(User).filter(User.username == username).first()
    if user is None:
        return False
    return True


def remove_online_user():
    user_id = session.get('user_id')
    if _check_online_user_exists(user_id):
        _remove_online_user(user_id)
        message = f"User {user_id} has been logout"
        log(message)
        return True, message
    message = f"User {user_id} has not been logged in"
    log(message)
    return False, message


def _check_user_exists(user_id):
    exists = db.session.query(User).filter(User.id == user_id).first()
    if exists is None:
        return False
    return True


def _check_online_user_exists(user_id):
    exists = db.session.query(Online_users).filter(Online_users.userId == user_id).first()
    if exists is None:
        return False
    return True


def _remove_user(user_id):
    db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()


def _remove_online_user(user_id):
    db.session.query(Online_users).filter(Online_users.userId == user_id).delete()
    db.session.commit()


def remove_user_from_db(user_id):
    if _check_user_exists(user_id):
        if _check_online_user_exists(user_id):
            _remove_online_user(user_id)
        _remove_user(user_id)
    else:
        return "User does not exist"
    message = f"User {user_id} removed succesfully"
    log(message)
    return message


def clear_session():
    session.clear()


def _check_updating_username(user, username):
    if user.username == username:
        return True
    exists = db.session.query(User).filter(User.username == username).first()
    if exists is None:
        return True
    return False


def _check_updating_email(user, email):
    if user.email == email:
        return True
    exists = db.session.query(User).filter(User.email == email).first()
    if exists is None:
        return True
    return False


def update_user(user_id, data):
    user = db.session.query(User).filter(User.id == user_id).first()
    if data.get("username") is not None:
        if not _check_updating_username(user, data["username"]):
            return "username already exists"
    if data.get("email") is not None:
        if not _check_updating_email(user, data["email"]):
            return "email already exists"
    if data.get("password") is not None:
        if not is_valid_password(data["password"]):
            return "Password does not meet the required regulations."
        data["password"] = hash_text(data["password"])
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    message = "user updated successfully"
    log(message)
    return message
