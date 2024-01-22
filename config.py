# config.py
import os
class configdb():
    SQLALCHEMY_DATABASE_URI =   'postgresql://postgres:postgres@localhost/flaskpdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'

