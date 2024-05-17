import json

from app import user_blueprint
from app.models.dbmodel import User, db
from app.services.user_services import create_logic, get_all_users
from flask import render_template, jsonify


@user_blueprint.route('/user/list', methods=['GET'])
def user_list():
    users = get_all_users()
    return render_template('user_list.html', users=users)


@user_blueprint.route('/api/user/list', methods=['GET'])
def api_user_list():
    users = get_all_users()
    return jsonify(users)


