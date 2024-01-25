import hashlib
import re
import uuid


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    pattern = r'^(?=.*[A-Za-z0-9]).{8,}$'

    if re.search(pattern, password):
        return True
    else:
        return False


def hash_text(text):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt


def check_hashed_text(hashed_text, provided_text):
    _hashedText, salt = hashed_text.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + provided_text.encode()).hexdigest()
