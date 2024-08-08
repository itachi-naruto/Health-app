from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import SeheduelService


schedules = Blueprint('schedules', __name__)

service = SeheduelService()

@schedules.route('/', methods=['GET'])
@cross_origin()
def get_schedules():
    return jsonify({'schedules': service.getSeheduels(None)})

# by doctor id 
@schedules.route('/<int:id>', methods=['GET'])
@cross_origin()
def get_doctor_schedule(id):
    return jsonify({'schedules': service.getSeheduels(id)})

@schedules.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_schedule(self):   
    message, status = service.createSeheduel(request.json)
    return jsonify({'msg': message, 'status': status}), status

@schedules.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_schedule(self, id):
    message, status = service.updateSchedule(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@schedules.route('/book/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def book_schedule(self, id):
    message, status = service.bookSchedule(id)
    return jsonify({'msg': message,'status':status}), status

@schedules.route('/cancel/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def cancel_schedule(self, id):
    message, status = service.cancelSchedule(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@schedules.route('/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_schedule(self, id):
    message, status = service.d(id)
    return jsonify({'msg': message,'status':status}), status