# models/dbmodel.py
import hashlib

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String)
    lastname = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Online_users(db.Model):
    __tablename__ = 'online_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ipaddress = db.Column(db.String, nullable=False)
    logindatetime = db.Column(db.DateTime, nullable=False)
