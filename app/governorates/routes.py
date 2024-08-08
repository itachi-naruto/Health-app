from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import LocationService


locations = Blueprint('locations', __name__)

service = LocationService()


# display all locations and wilayats

@locations.route('/', methods=['GET'])
@cross_origin()
# @roles.token_required
def get_locations():
    return jsonify({'locations': service.getlocations()})

@locations.route('/wilayats', methods=['GET'])
@cross_origin()
# @roles.token_required
def get_wilayats():
    return jsonify({'Wilayats': service.getWilayats()})

@locations.route('/<int:id>', methods=['GET'])
@cross_origin()
# @roles.token_required
def getGovernorate(id):
    message, status = service.getGovernorateById(id)
    return jsonify({'msg':message,'status':status}), status

@locations.route('/wilayats/<int:id>', methods=['GET'])
@cross_origin()
# @roles.token_required
def getWilayat(id):
    message, status = service.getWilayatById(id)
    return jsonify({'msg':message,'status':status}), status


# adding locations and wilayats

@locations.route('/addGovernorate', methods=['POST'])
@cross_origin()
# @roles.token_required
def add_locations():  
    if not request.json:
        abort(404)
    message, status = service.addGovernorate(request.json)  
    return jsonify({'msg': message}), status

@locations.route('/addWilayat', methods=['POST'])
@cross_origin()
# @roles.token_required
def add_wilayats():  
    if not request.json:
        abort(404)
    message, status = service.addWilayat(request.json)  
    return jsonify({'msg': message}), status

