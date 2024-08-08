## service layer of the API
import json
import sqlalchemy as sql
from flask import current_app
from datetime import datetime
from sqlalchemy.orm.query import Query
from config import BaseConfig
from sqlalchemy import func

from app.doctors.model import Doctor
from app.centers.model import Center
from app.patients.model import Patient

from .model import Review

class ReviewService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getReviews(self, id): 
        try:
            if id is None:
                reviews = self.session.query(Review, Doctor, Patient, Center).join(Doctor, Doctor.user_id == Review.reviewer_id , isouter=True).join(Center, Center.user_id == Review.reviewer_id , isouter=True).join(Patient, Patient.user_id == Review.reviewer_id , isouter=True).all()
            else:
                reviews = self.session.query(Review, Doctor, Patient, Center).join(Doctor, Doctor.user_id == Review.reviewer_id , isouter=True).join(Center, Center.user_id == Review.reviewer_id , isouter=True).join(Patient, Patient.user_id == Review.reviewer_id , isouter=True).filter(Review.id==id).all()
            
            result = []

            for review in reviews:
                data = {}
                data['id'] = review.Review.id
                data['title'] = review.Review.title
                data['description'] = review.Review.description
                data['doctor_review'] = review.Review.doctor_review
                data['center_review'] = review.Review.center_review
                data['patient_review'] = review.Review.patient_review
                data['reviewed'] = review.Review.reviewed
                data['reply_to'] = review.Review.reply_to
                data['reviewer_id'] = review.Review.reviewer_id
                data['reviewer_name_d'] = None if review.Doctor is None else review.Doctor.first_name
                data['reviewer_name_c'] = None if review.Center is None else review.Center.name
                data['reviewer_name_p'] = None if review.Patient is None else review.Patient.first_name 
                data['doctor_id'] = review.Review.doctor_id
                data['center_id'] = review.Review.center_id
                data['patient_id'] = review.Review.patient_id
                data['review_date'] = review.Review.review_date

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()


    def getDoctorReviews(self, id): 
        try:
            dr_reviews = self.session.query(func.count(Review.doctor_review).label("reviews")).filter(Review.doctor_id==id).first()
            
            return dr_reviews.reviews if dr_reviews is not None else 0
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()
    
    def getDoctorRate(self, id): 
        try:
            dr_rate = self.session.query(func.count(Review.doctor_review).label("reviews"), func.sum(Review.doctor_review).label("rate")).filter(Review.doctor_id==id).first()
            
            rate = 0

            if dr_rate:
                if dr_rate.reviews and dr_rate.rate:
                    rate = int(dr_rate.rate / dr_rate.reviews)

            return rate
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()

    def getCenterReviews(self, id): 
        try:
            cr_reviews = self.session.query(func.count(Review.center_review).label("reviews")).filter(Review.center_id==id).first()
            
            return cr_reviews.reviews if cr_reviews is not None else 0
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()

    def getCenterRate(self, id): 
        try:
            cr_rate = self.session.query(func.count(Review.center_review).label("reviews"), func.sum(Review.center_review).label("rate")).filter(Review.center_id==id).first()
            
            rate = 0

            if cr_rate:
                if cr_rate.reviews and cr_rate.rate:
                    rate = int(cr_rate.rate / cr_rate.reviews)

            return rate
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()

    def createReview(self, data):
        try:
            review = Review(title=data['title'],
            description=data['description'],
            doctor_review=data['doctor_review'],
            center_review=data['center_review'],
            patient_review=data['patient_review'],
            review_date=datetime.now(),
            reply_to=data['reply_to'],
            reviewer_id=data['reviewer_id'],
            doctor_id=data['doctor_id'],
            center_id=data['center_id'],
            patient_id=data['patient_id'])

            self.session.add(review)
            self.session.commit()

            return 'Created', 201
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
            
    def updateReview(self, id, data):
        try:
            review = self.session.query(Review).filter(Review.id==id).first()

            review.title = data['title']
            review.description = data['description']
            review.doctor_review = data['doctor_review']
            review.center_review = data['center_review']
            review.patient_review = data['patient_review']
            review.reply_to = data['reply_to']
            review.reviewer_id = data['reviewer_id']
            review.doctor_id = data['doctor_id']
            review.center_id = data['center_id']
            review.patient_id = data['patient_id']
            review.review_date = datetime.now()

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def deleteReview(self, id):
        try:
            review = self.session.query(Review).filter(Review.id==id).first()

            if review == None:
                return 'Not Found', 404
            
            self.session.delete(review)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getReviewsByDoctorID(self, id): 
        try:
            reviews = self.session.query(Review, Doctor, Patient).join(Doctor, Doctor.user_id==Review.reviewer_id, isouter=True).join(Patient, Patient.user_id==Review.reviewer_id, isouter=True).filter(Review.doctor_id==id).all()
            
            result = []

            for review in reviews:
                data = {}
                data['id'] = review.Review.id
                data['title'] = review.Review.title
                data['description'] = review.Review.description
                data['doctor_review'] = review.Review.doctor_review
                data['reviewed'] = review.Review.reviewed
                data['reply_to'] = review.Review.reply_to
                data['reviewer_id'] = review.Review.reviewer_id
                data['reviewer_name_d'] = None if review.Doctor is None else review.Doctor.first_name
                data['reviewer_name_p'] = None if review.Patient is None else review.Patient.first_name 
                data['doctor_id'] = review.Review.doctor_id
                data['review_date'] = review.Review.review_date

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getReviewsByPatientID(self, id): 
        try:
            reviews = self.session.query(Review, Doctor, Patient).join(Doctor, Doctor.user_id==Review.reviewer_id, isouter=True).join(Patient, Patient.user_id==Review.reviewer_id, isouter=True).filter(Review.patient_id==id).all()
            
            result = []

            for review in reviews:
                data = {}
                data['id'] = review.Review.id
                data['title'] = review.Review.title
                data['description'] = review.Review.description
                data['patient_review'] = review.Review.patient_review
                data['reviewed'] = review.Review.reviewed
                data['reply_to'] = review.Review.reply_to
                data['reviewer_id'] = review.Review.reviewer_id
                data['reviewer_name_d'] = None if review.Doctor is None else review.Doctor.first_name
                data['reviewer_name_p'] = None if review.Patient is None else review.Patient.first_name 
                data['doctor_id'] = review.Review.doctor_id
                data['patient_id'] = review.Review.patient_id
                data['review_date'] = review.Review.review_date

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()