from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import UserService


users = Blueprint('users', __name__)

service = UserService()

@users.route('/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_users(self):
    return jsonify({'users': service.getUsers()})

@users.route('/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_user(self, id):
    message, status = service.get_user_by_id(id)
    return jsonify({'msg':message,'status':status}), status

@users.route('/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_user(self, id):
    message, status = service.deleteUser(id)
    return jsonify({'msg': message,'status':status}), status

@users.route('/disable/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def disable_user(self, id):
    message, status = service.disableUser(id)
    return jsonify({'msg': message,'status':status}), status

@users.route('/enable/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def enable_user(self, id):
    message, status = service.enableUser(id)
    return jsonify({'msg': message,'status':status}), status

@users.route('/roles/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_roles(self):
    return jsonify({'roles': service.getRoles()})


@users.route('/logs/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_logs(self):
    return jsonify({'logs': service.showLogins()})