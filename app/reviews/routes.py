from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response

from app.security import roles

from .service import ReviewService


reviews = Blueprint('reviews', __name__)

service = ReviewService()

# --- get --- #
@reviews.route('/', methods=['GET'])
@cross_origin()
def get_reviews():
    return jsonify({'reviews': service.getReviews(None)})

@reviews.route('/<int:id>', methods=['GET'])
@cross_origin()
def get_review(id):
    return jsonify({'reviews': service.getReviews(id)})

@reviews.route('/by_doctor_id/<int:id>', methods=['GET'])
@cross_origin()
def get_reviews_by_doctor(id):
    return jsonify({'reviews': service.getReviewsByDoctorID(id)})

@reviews.route('/by_patient_id/<int:id>', methods=['GET'])
@cross_origin()
def get_reviews_by_patient(id):
    return jsonify({'reviews': service.getReviewsByPatientID(id)})


# --- add --- #
@reviews.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def add_review(self):
    if not request.json:
        abort(404)    
    message, status = service.createReview(request.json)
    return jsonify({'msg': message, 'status': status}), status

# --- update --- #
@reviews.route('/<int:id>', methods=['PATCH'])
@cross_origin()
@roles.token_required
def update_review(self, id):
    message, status = service.updateReview(id, request.json)
    return jsonify({'msg': message}), status

# --- delete --- #
@reviews.route('/<int:id>', methods=['DELETE'])
@cross_origin()
@roles.role_required(['admin'])
def delete_review(self, id):
    message, status = service.deleteReview(id)
    return jsonify({'msg': message}), status