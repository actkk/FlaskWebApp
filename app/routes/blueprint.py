from flask import render_template, request, Blueprint
from app.services.user_services import get_all_users, clear_session, remove_online_user, user_login, get_online_users, \
    create_new_user, remove_user_from_db, update_user, check_username_exists
from app.services.general_services import is_valid_password, is_valid_email

user_blueprint = Blueprint('user', __name__, template_folder='templates', static_folder='static')


# todo yanlış ve geçersiz şifre email girişlerinde responsları düzenle

@user_blueprint.route('/user/list')
def user_list():
    users = get_all_users()
    return render_template('user_list.html', users=users)


@user_blueprint.route('/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Extract data from
        # todo requesti service kısmında hallet
        username = request.form['username']
        firstname = request.form['firstname']
        middlename = request.form.get('middlename')
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            return "Invalid format for email address"
        if not is_valid_password(password):
            return "Invalid format for password\nPassword complexity should be least [A-Za-z0-9] and min 8 characters."
        if check_username_exists(username):
            return "Username already exists"
        user_created = create_new_user(username, firstname, middlename, lastname, birthdate, email, password)

        if user_created:
            return "User created successfully"

    return render_template('create_user.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract username and password from form data
        email = request.form['email']
        password = request.form['password']

        # Authenticate the user
        success, message = user_login(email, password)

        if success:
            return "User logged in", 200
        else:
            return message

    return render_template('login.html')


@user_blueprint.route('/onlineusers')
def onlineusers():
    return render_template('onlineusers.html', users=get_online_users())


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if remove_online_user():
            clear_session()
            return "User successfully removed from online users.", 200
        else:
            return "Error in removing user from online users."

    return render_template('logout.html')


@user_blueprint.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return remove_user_from_db(user_id)


@user_blueprint.route('/user/update/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json

    message = update_user(user_id, data)
    return message


@user_blueprint.route('/')
def home():
    return render_template('home.html')


@user_blueprint.route('/horse')
def horse():
    return render_template('horse.html')