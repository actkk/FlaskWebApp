from flask import Blueprint, render_template

user_blueprint = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_blueprint.route('/user/list')
def user_list():
    return render_template('user_list.html')

@user_blueprint.route('/user/create')
def create_user():
    return render_template('create_user.html')

@user_blueprint.route('/login')
def login():
    return render_template('login.html')
