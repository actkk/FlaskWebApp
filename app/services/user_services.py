from app import db
from app.models.dbmodel import User,Online_users, db
import re
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
def list_all_users():
    return db.get_or_404(User)

