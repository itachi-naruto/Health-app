from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response,send_from_directory

from app.security import roles

from .service import SpecialtyService
import json
from config import FileUploadConfig
specialties = Blueprint('specialties', __name__)

service = SpecialtyService()

@specialties.route('/', methods=['GET'])
@cross_origin()
def get_specialties():
    return jsonify({'specialties': service.getSpecialties(None)})

@specialties.route('/<int:id>', methods=['GET'])
@cross_origin()
def get_specialty(id):
    return jsonify({'specialties': service.getSpecialties(id)})


@specialties.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_specialty(self):
	if 'file' not in request.files:
		print('error no file')
		response = jsonify({'message': 'No file part in the request'})
		response.status_code = 400
		return response
	if not request.form:
		print('error no form')
		abort(400)

	dictionary = request.form.to_dict(flat=False)
	list = dictionary['form']
	param = json.loads(list[0])
	
	message = service.createspecialty(request.files.getlist('file'), param)
	return jsonify({'msg': message}), 201
# def add_specialty(self):
#     if not request.json or not 'name' in request.json:
#         abort(404)    
#     message, status = service.createspecialty(request.json)
#     return jsonify({'msg': message, 'status': status}), status
@specialties.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_specialty(self, id):
    message, status = service.updateSpecialty(id, request.json)
    return jsonify({'msg': message}), status

@specialties.route('/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_specialty(self, id):
    message, status = service.deleteSpecialty(id)
    return jsonify({'msg': message}), status

@specialties.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(FileUploadConfig.UPLOAD_FOLDER, filename)