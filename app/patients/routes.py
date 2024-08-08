from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import PatientService


patients = Blueprint('patients', __name__)

service = PatientService()

@patients.route('/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_patients(self):
    return jsonify({'patients': service.getPatients(None),'status':200})

@patients.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_patients(self):
    message, status = service.add_patient(request.json)
    return jsonify({'msg':message,'status':status}), status

@patients.route('/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_patient(self, id):
    return jsonify({'patients': service.getPatients(id),'status':200})

@patients.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.update_token_required
def update_patient(self, id):
    message, status = service.updatePatient(id, request.json)
    return jsonify({'msg': message,'status':status}), status

# ----- Dependents ------ #
@patients.route('/dependet/<int:parent_id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_dependets(self, parent_id):
    return jsonify({'dependets': service.get_dependents(parent_id, None),'status':200})

@patients.route('/dependet/<int:parent_id>/<int:patient_id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_dependet(self, parent_id, patient_id):
    return jsonify({'dependets': service.get_dependents(parent_id, patient_id)})

@patients.route('/dependet/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def add_patient_dependent(self, id):
    message, status = service.add_dependent(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@patients.route('/update_dependet/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_dependet(self, id):
    message, status = service.update_dependent(id, request.json)
    return jsonify({'msg': message,'status':status}), status

@patients.route('/delete_dependet/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_dependet(self, id):
    message, status = service.delete_dependent(id)
    return jsonify({'msg': message,'status':status}), status
