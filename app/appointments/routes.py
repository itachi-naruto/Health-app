from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import AppointmentService


appointments = Blueprint('appointments', __name__)

service = AppointmentService()

# --- get --- #
@appointments.route('/', methods=['GET'])
@cross_origin()
def get_appointments():
    response, status = service.getAppointments(None)
    return jsonify({'appointments':response }), status

@appointments.route('/<int:id>', methods=['GET'])
@cross_origin()
def get_appointment(id):
    response, status = service.getAppointments(id)
    return jsonify({'appointments':response }), status

@appointments.route('/doctor/<int:id>', methods=['GET'])
@cross_origin()
def get_doctor_appointments(id):
    return jsonify({'appointments': service.getDoctorAppointments(id)})

@appointments.route('/doctor/patients/<int:id>', methods=['GET'])
@cross_origin()
def get_doctor_patients(id):
    return jsonify({'appointments': service.getDoctorPatients(id)})

@appointments.route('/patient/<int:id>', methods=['GET'])
@cross_origin()
def get_patient_appointments(id):
    return jsonify({'appointments': service.getPatientAppointments(id)})

@appointments.route('/center/<int:id>', methods=['GET'])
@cross_origin()
def get_center_appointments(id):
    return jsonify({'appointments': service.getCenterAppointments(id)})

# --- add --- #
@appointments.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_appointments(self):
    if not request.json or not 'date' in request.json:
        abort(404)    
    id, status = service.createAppointment(request.json)
    return jsonify({'id': id, 'status': status}), status

# --- update --- #
@appointments.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_appointments(self, id):
    message, status = service.updateAppointment(id, request.json)
    return jsonify({'msg': message}), status

@appointments.route('/update_status/<int:id>/<int:status_id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_appointment_status(self, id, status_id):
    message, status = service.updateAppointmentStatus(id, status_id)
    return jsonify({'msg': message}), status

# --- delete --- #
@appointments.route('/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_appointments(self, id):
    message, status = service.deleteAppointment(id, False)
    return jsonify({'msg': message}), status