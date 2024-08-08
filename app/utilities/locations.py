## service layer of the API
import sqlalchemy as sql
from flask import current_app, Blueprint, request, jsonify
from app.security import roles
from datetime import datetime
from config import BaseConfig
from datetime import datetime, date
from sqlalchemy import or_, func
from flask_cors import CORS, cross_origin
from app.users.model import User, Role
from app.oman_governorates.model import Governorate, Wilayat, City, Area
from app.status.model import Status
from app.doctors.model import Doctor
from app.payment_transaction.model import PaymentTransaction

## locations ##
locations = Blueprint('locations', __name__)
def __init__(self):
    self.eng = BaseConfig().engine

    # Create a session
    self.Session = sql.orm.sessionmaker()
    self.Session.configure(bind=self.eng)
    self.session = self.Session()

@locations.route('/')
def index():
    return "Oman Geographic Data API"

### Governorate Routes ###

@locations.route('/governorates', methods=['GET'])
@cross_origin()
@roles.token_required
def get_governorates():
    governorates = Governorate.query.all()
    return jsonify([{'id': gov.id, 'name': gov.name} for gov in governorates])

@locations.route('/governorates/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_governorate(id):
    governorate = Governorate.query.get_or_404(id)
    wilayats = [{'id': wil.id, 'name': wil.name} for wil in governorate.wilayats]
    return jsonify({'id': governorate.id, 'name': governorate.name, 'wilayats': wilayats})

@locations.route('/governorates', methods=['POST'])
@cross_origin()
@roles.token_required
def create_governorate(self):
    data = request.get_json()
    new_governorate = Governorate(name=data['name'])
    self.session.add(new_governorate)
    self.session.commit()
    return jsonify({'id': new_governorate.id, 'name': new_governorate.name}), 201

@locations.route('/governorates/<int:id>', methods=['PUT'])
@cross_origin()
@roles.token_required
def update_governorate(self, id):
    data = request.get_json()
    governorate = Governorate.query.get_or_404(id)
    governorate.name = data['name']
    self.session.commit()
    return jsonify({'id': governorate.id, 'name': governorate.name})

@locations.route('/governorates/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_governorate(self, id):
    governorate = Governorate.query.get_or_404(id)
    self.session.delete(governorate)
    self.session.commit()
    return jsonify({'message': 'Governorate deleted successfully'})

### Wilayat Routes ###

@locations.route('/wilayats', methods=['GET'])
@cross_origin()
@roles.token_required
def get_wilayats():
    wilayats = Wilayat.query.all()
    return jsonify([{'id': wil.id, 'name': wil.name, 'governorate_id': wil.governorate_id} for wil in wilayats])

@locations.route('/wilayats/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_wilayat(id):
    wilayat = Wilayat.query.get_or_404(id)
    cities = [{'id': city.id, 'name': city.name} for city in wilayat.cities]
    return jsonify({'id': wilayat.id, 'name': wilayat.name, 'governorate_id': wilayat.governorate_id, 'cities': cities})

@locations.route('/wilayats', methods=['POST'])
@cross_origin()
@roles.token_required
def create_wilayat(self):
    data = request.get_json()
    new_wilayat = Wilayat(name=data['name'], governorate_id=data['governorate_id'])
    self.session.add(new_wilayat)
    self.session.commit()
    return jsonify({'id': new_wilayat.id, 'name': new_wilayat.name, 'governorate_id': new_wilayat.governorate_id}), 201

@locations.route('/wilayats/<int:id>', methods=['PUT'])
@cross_origin()
@roles.token_required
def update_wilayat(self,id):
    data = request.get_json()
    wilayat = Wilayat.query.get_or_404(id)
    wilayat.name = data['name']
    wilayat.governorate_id = data['governorate_id']
    self.session.commit()
    return jsonify({'id': wilayat.id, 'name': wilayat.name, 'governorate_id': wilayat.governorate_id})

@locations.route('/wilayats/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_wilayat(self, id):
    wilayat = Wilayat.query.get_or_404(id)
    self.session.delete(wilayat)
    self.session.commit()
    return jsonify({'message': 'Wilayat deleted successfully'})

### City Routes ###

@locations.route('/cities', methods=['GET'])
@cross_origin()
@roles.token_required
def get_cities():
    cities = City.query.all()
    return jsonify([{'id': city.id, 'name': city.name, 'wilayat_id': city.wilayat_id} for city in cities])

@locations.route('/cities/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_city(id):
    city = City.query.get_or_404(id)
    areas = [{'id': area.id, 'name': area.name} for area in city.areas]
    return jsonify({'id': city.id, 'name': city.name, 'wilayat_id': city.wilayat_id, 'areas': areas})

@locations.route('/cities', methods=['POST'])
@cross_origin()
@roles.token_required
def create_city(self):
    data = request.get_json()
    new_city = City(name=data['name'], wilayat_id=data['wilayat_id'])
    self.session.add(new_city)
    self.session.commit()
    return jsonify({'id': new_city.id, 'name': new_city.name, 'wilayat_id': new_city.wilayat_id}), 201

@locations.route('/cities/<int:id>', methods=['PUT'])
@cross_origin()
@roles.token_required
def update_city(self, id):
    data = request.get_json()
    city = City.query.get_or_404(id)
    city.name = data['name']
    city.wilayat_id = data['wilayat_id']
    self.session.commit()
    return jsonify({'id': city.id, 'name': city.name, 'wilayat_id': city.wilayat_id})

@locations.route('/cities/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_city(self, id):
    city = City.query.get_or_404(id)
    self.session.delete(city)
    self.session.commit()
    return jsonify({'message': 'City deleted successfully'})

### Area Routes ###

@locations.route('/areas', methods=['GET'])
@cross_origin()
@roles.token_required
def get_areas():
    areas = Area.query.all()
    return jsonify([{'id': area.id, 'name': area.name, 'city_id': area.city_id} for area in areas])

@locations.route('/areas/<int:id>', methods=['GET'])
@cross_origin()
@roles.token_required
def get_area(id):
    area = Area.query.get_or_404(id)
    return jsonify({'id': area.id, 'name': area.name, 'city_id': area.city_id})

@locations.route('/areas', methods=['POST'])
@cross_origin()
@roles.token_required
def create_area(self):
    data = request.get_json()
    new_area = Area(name=data['name'], city_id=data['city_id'])
    self.session.add(new_area)
    self.session.commit()
    return jsonify({'id': new_area.id, 'name': new_area.name, 'city_id': new_area.city_id}), 201

@locations.route('/areas/<int:id>', methods=['PUT'])
@cross_origin()
@roles.token_required
def update_area(self, id):
    data = request.get_json()
    area = Area.query.get_or_404(id)
    area.name = data['name']
    area.city_id = data['city_id']
    self.session.commit()
    return jsonify({'id': area.id, 'name': area.name, 'city_id': area.city_id})

@locations.route('/areas/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.token_required
def delete_area(self, id):
    area = Area.query.get_or_404(id)
    self.session.delete(area)
    self.session.commit()
    return jsonify({'message': 'Area deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)