from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import DoctorService


doctors = Blueprint('doctors', __name__)

service = DoctorService()

@doctors.route('/', methods=['GET'])
@cross_origin()
def get_doctors():
    return jsonify({'doctors': service.getDoctors(None)})

@doctors.route('/', methods=['POST'])
@cross_origin()
def add_doctors():
    message, status = service.add_doctor(request.json)
    return jsonify({'msg':message,'status':status}), status

@doctors.route('/<int:id>', methods=['GET'])
@cross_origin()
def get_doctor(id):
    return jsonify({'doctors': service.getDoctors(id),'status':200})

@doctors.route('/in_center/<int:center_id>', methods=['GET'])
@cross_origin()
def get_doctors_in_center(center_id):
    return jsonify({'doctors': service.getDoctorsInMedicalCenter(center_id),'status':200})

# ----------------------------------------- #
# get all doctors for admin dashboard 
@doctors.route('/admin', methods=['GET'])
@cross_origin()
def get_doctors_admin():
    return jsonify({'doctors': service.getDoctors_admin(None)})

@doctors.route('/admin/<int:id>', methods=['GET'])
@cross_origin()
def get_doctor_admin(id):
    return jsonify({'doctors': service.getDoctors_admin(id),'status':200})
# ----------------------------------------- #

@doctors.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_doctor(self, id):
    message, status = service.updateDoctor(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@doctors.route('/image/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.update_token_required
def update_doctor_image(self, id):
    message, status = service.updateImage(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@doctors.route('/approve/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def approve_doctor(self, id):
    message, status = service.approveDoctor(id)
    return jsonify({'msg': message,'status':status}), status

@doctors.route('/disable/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def disable_doctor(self, id):
    message, status = service.disableDoctor(id)
    return jsonify({'msg': message,'status':status}), status


# ------------------------------------- #
@doctors.route('/joinCenter/<int:doctor_id>/<int:center_id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def join_doctor_to_center(self, doctor_id, center_id):
    message, status = service.joinHospital(doctor_id, center_id)
    return jsonify({'msg': message,'status':status}), status


@doctors.route('/centers/<int:doctor_id>', methods=['GET'])
@cross_origin()
def get_doctor_to_center(doctor_id):
    return jsonify({'centers': service.getDoctorCenters(doctor_id),'status':200})

@doctors.route('/center/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_center_doctors(self, id):
    return jsonify({'doctors': service.getCenterDoctors(id),'status':200})

# get all getDoctorHistory
@doctors.route('/history', methods=['GET'])
@cross_origin()
@roles.token_required
def get_doctors_history(self):
    history, status = service.getAllDoctorHistory()
    return jsonify({'history': history,'status':status}), status

# get getDoctorHistory for admin dashboard
@doctors.route('/history/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_doctor_history(self, id):
    history, status = service.getDoctorHistory(id)
    return jsonify({'history': history,'status':status}), status