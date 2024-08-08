import jwt

from flask import g, request, jsonify, abort, make_response
from werkzeug.security import check_password_hash
from functools import wraps

from app.users.service import UserService
from config import SecretKey

user_service = UserService()
SECRET_KEY = SecretKey().SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, "HS256")
            current_user = user_service.getUserByPublicID(data['public_id'])
            g.user = current_user
        except Exception as e:
            return jsonify({'message': 'token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorator

def update_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        id = kwargs['id']

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, "HS256")
            current_user = user_service.getUserByPublicIDWithRole(data['public_id'])
            
            if current_user.Role.name.lower() != 'admin':
                if current_user.User.id != id:
                    return jsonify({'message': 'You dont have permission to access this resource.'}), 401
            g.user = current_user
        except Exception as e:
            return jsonify({'message': 'token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorator

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, "HS256")
                
                current_user = user_service.getUserByPublicID(data['public_id'])
                user_role = user_service.getRole(current_user.role_id)

                if user_role not in role:
                    return jsonify({'message': 'You dont have permission to access this resource.'}), 401
                g.user = current_user
                
            except Exception as e:
                return jsonify({'message': 'token is invalid'}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator