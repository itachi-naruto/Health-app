from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import SettingService


settings = Blueprint('settings', __name__)

service = SettingService()

@settings.route('/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_all_settings(self):
    return jsonify({'settings': service.getSettings()})

@settings.route('/<key>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_setting(key):
    settings = service.getSettings(key)
    return jsonify({'settings': settings})

@settings.route('/category/<category>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_setting_by_category(category):
    settings = service.getSettingsByCategory(category)
    return jsonify({'settings': settings})

@settings.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_setting():
    if not request.json or not 'key' in request.json:
        abort(404)    
    message, status = service.createSetting(request.json)
    return jsonify({'msg': message}), status

@settings.route('/<key>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_setting(key):
    message, status = service.updateSetting(key, request.json)
    return jsonify({'msg': message}), status


@settings.route('/<key>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_setting(key):
    message, status = service.deleteSetting(key)
    return jsonify({'msg': message}), status
