from flask import Blueprint, render_template, flash
from flask import render_template, request, redirect, url_for
from app.services.user_services import get_all_users, clear_session, remove_online_user, user_login, get_online_users, create_new_user, remove_user_from_db
from app.services.general_services import is_valid_password , is_valid_email
user_blueprint = Blueprint('user', __name__, template_folder='templates', static_folder='static')




@user_blueprint.route('/user/list')
def user_list():
    users = get_all_users()
    return render_template('user_list.html', users=users)


@user_blueprint.route('/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Extract data from form
        username = request.form['username']
        firstname = request.form['firstname']
        middlename = request.form.get('middlename')
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            flash('Invalid email address', 'error')
            return render_template('create_user.html')
        if not is_valid_password(password):
            flash('Invalid password', 'error')
            return render_template('create_user.html')
        # Delegate the creation logic to the service
        user_created = create_new_user(username, firstname, middlename, lastname, birthdate, email, password)

        if user_created:
            return redirect("/user/list")

        # Handle the case where user creation fails, if necessary

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
            # Redirect to a home page or dashboard after successful login
            return redirect("/onlineusers")
        else:
            # Flash a message and re-render the login page if login fails
            flash(message)
            return redirect("/user/list")

    # Render the login page for GET requests
    return render_template('login.html')

@user_blueprint.route('/onlineusers')
def onlineusers():
    return render_template('onlineusers.html',users=get_online_users())



@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if remove_online_user():
            print("User successfully removed from online users.")
        else:
            print("Error in removing user from online users.")

        clear_session()
        return redirect('/onlineusers')  # Redirect to login page or home page

    # Render the logout page with a button for GET request
    return render_template('logout.html')


@user_blueprint.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return remove_user_from_db(user_id)
