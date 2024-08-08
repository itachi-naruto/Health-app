## service layer of the API
import json
import sqlalchemy as sql
from flask import current_app
from sqlalchemy.orm.query import Query
from config import BaseConfig
from .model import Doctor, DoctorHistory

from app.utilities.request_utils import not_exisit_in_request, to_datetime

from app.users.model import User
from app.centers.model import Center, CenetrDoctors
from app.schedules.service import SeheduelService
from app.reviews.service import ReviewService

class DoctorService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getDoctors(self, id): 
        try:
            if id is None:
                doctors = self.session.query(Doctor, User).filter(Doctor.user_id==User.id).filter(Doctor.approved==True).all()
            else:
                doctors = self.session.query(Doctor, User).filter(Doctor.user_id==User.id).filter(Doctor.approved==True).filter(Doctor.user_id==id).all()
            
            result = []

            for doctor in doctors:
                data = {}
                data['id'] = doctor.Doctor.user_id
                data['public_id'] = doctor.User.public_id
                data['doctor_id'] = doctor.Doctor.id
                data['first_name'] = doctor.Doctor.first_name
                data['last_name'] = doctor.Doctor.last_name
                data['gender'] = doctor.Doctor.gender
                data['birth_date'] = doctor.Doctor.birth_date
                data['blood_type'] = doctor.Doctor.blood_type.upper()
                data['country'] = doctor.Doctor.country
                data['address'] = doctor.Doctor.address
                data['place_location'] = doctor.Doctor.place_location
                data['exact_location'] = doctor.Doctor.exact_location
                data['speciality'] = doctor.Doctor.speciality
                data['professional_experiance'] = doctor.Doctor.professional_experiance
                data['certification'] = doctor.Doctor.certification
                data['experiance'] = doctor.Doctor.experiance
                data['education'] = doctor.Doctor.education
                data['memberships'] = doctor.Doctor.memberships
                data['follow_up_fee'] = 0 if doctor.Doctor.follow_up_fee is None else float(doctor.Doctor.follow_up_fee)
                data['consultation_fee'] = 0 if doctor.Doctor.consultation_fee is None else float(doctor.Doctor.consultation_fee)
                data['biography'] = doctor.Doctor.biography
                data['medical_board_registrations'] = doctor.Doctor.medical_board_registrations
                data['know_languages'] = doctor.Doctor.know_languages
                data['image'] = doctor.Doctor.image
                data['next_available'] = SeheduelService().getNextScheduel((doctor.Doctor.id))
                data['dr_reviews'] = ReviewService().getDoctorReviews((doctor.Doctor.id))
                data['dr_rate'] = ReviewService().getDoctorRate((doctor.Doctor.id))
                data['email'] = doctor.User.email
                data['phone'] = doctor.User.phone
                data['contract_sign'] = doctor.Doctor.contract_sign
                data['notes'] = doctor.Doctor.notes

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def add_doctor(self, data):
        try:
            if not data or not 'civil_id' in data:
              return 'civil id is required', 401
            
            if not data or not 'first_name' in data:
              return 'First name is required', 401
            
            if not data or not 'blood_type' in data:
              return 'Blood type is required', 401
          
            if not data or not 'user_id' in data:
              return 'user is required', 401
            
            user = self.session.query(User).filter(User.id == data['user_id']).first()
            if user is None:
               return 'User not found',  404
            
            user_doctor = self.session.query(Doctor).filter(Doctor.user_id == data['user_id']).first()
            if user_doctor:
               return 'The doctor already has a profile.',  200
            
            doctor = Doctor(first_name=data['first_name'], 
                            last_name=data['last_name'],
                            gender=data['gender'],
                            user_id=data['user_id'],
                            birth_date=to_datetime(data['birth_date']),
                            blood_type=data['blood_type'],
                            country=data['nationality'],
                            address=data['address'],
                            speciality=data['speciality'],
                            # place_location=data['place_location'],
                            # exact_location=data['exact_location'],
                            # professional_experiance= '' if data['professional_experiance'] is None else  data['professional_experiance'],
                            # certification=data['certification'],
                            # experiance=data['experiance'],
                            # education=data['education'],
                            # memberships=data['memberships'],
                            # biography=data['biography'],
                            follow_up_fee=data['follow_up_fee'],
                            consultation_fee=data['consultation_fee'],
                            medical_board_registrations=data['medical_board_registrations'],
                            know_languages=data['know_languages'])
            self.session.add(doctor)
            self.session.commit()
            if doctor:
                   return "Doctor is Created", 201

        except Exception as e:
            current_app.logger.error(e)
            self.session.rollback()
            return "{}".format("Internal Server Error"), 500
        finally:
            self.session.close()

    def getDoctorsInMedicalCenter(self, center_id): 
        try:
            doctors = self.session.query(Doctor, CenetrDoctors).filter(Doctor.approved==True).filter(CenetrDoctors.center_id==center_id).all()
            
            result = []

            for doctor in doctors:
                data = {}
                data['id'] = doctor.Doctor.user_id
                data['doctor_id'] = doctor.Doctor.id
                data['first_name'] = doctor.Doctor.first_name
                data['last_name'] = doctor.Doctor.last_name
                data['gender'] = doctor.Doctor.gender
                data['birth_date'] = doctor.Doctor.birth_date
                data['blood_type'] = doctor.Doctor.blood_type.upper()
                data['country'] = doctor.Doctor.country
                data['address'] = doctor.Doctor.address
                data['place_location'] = doctor.Doctor.place_location
                data['exact_location'] = doctor.Doctor.exact_location
                data['speciality'] = doctor.Doctor.speciality
                data['professional_experiance'] = doctor.Doctor.professional_experiance
                data['certification'] = doctor.Doctor.certification
                data['experiance'] = doctor.Doctor.experiance
                data['education'] = doctor.Doctor.education
                data['memberships'] = doctor.Doctor.memberships
                data['follow_up_fee'] = 0 if doctor.Doctor.follow_up_fee is None else float(doctor.Doctor.follow_up_fee)
                data['consultation_fee'] = 0 if doctor.Doctor.consultation_fee is None else float(doctor.Doctor.consultation_fee)
                data['biography'] = doctor.Doctor.biography
                data['medical_board_registrations'] = doctor.Doctor.medical_board_registrations
                data['know_languages'] = doctor.Doctor.know_languages
                data['image'] = doctor.Doctor.image
                data['contract_sign'] = doctor.Doctor.contract_sign
                data['notes'] = doctor.Doctor.notes

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    # join example
    # doctors = self.session.query(Doctor, User, Center).join(CenetrDoctors, Doctor.id==CenetrDoctors.doctor_id, isouter=True).join(Center, Center.id==CenetrDoctors.center_id, isouter=True).filter(Doctor.user_id==User.id).all()
    # ------------------------------
    def getDoctors_admin(self, id): 
        try:
            if id is None:
                doctors = self.session.query(Doctor, User).filter(Doctor.user_id==User.id).all()
            else:
                doctors = self.session.query(Doctor, User).filter(Doctor.user_id==User.id).filter(Doctor.user_id==id).all()
            
            result = []

            for doctor in doctors:
                data = {}
                data['id'] = doctor.Doctor.user_id
                data['doctor_id'] = doctor.Doctor.id
                data['first_name'] = doctor.Doctor.first_name
                data['last_name'] = doctor.Doctor.last_name
                data['gender'] = doctor.Doctor.gender
                data['birth_date'] = doctor.Doctor.birth_date
                data['blood_type'] = doctor.Doctor.blood_type.upper() if doctor.Doctor.blood_type is not None else None
                data['country'] = doctor.Doctor.country
                data['address'] = doctor.Doctor.address
                data['place_location'] = doctor.Doctor.place_location
                data['exact_location'] = doctor.Doctor.exact_location
                data['speciality'] = doctor.Doctor.speciality
                data['professional_experiance'] = doctor.Doctor.professional_experiance
                data['certification'] = doctor.Doctor.certification
                data['experiance'] = doctor.Doctor.experiance
                data['education'] = doctor.Doctor.education
                data['memberships'] = doctor.Doctor.memberships
                data['follow_up_fee'] = 0 if doctor.Doctor.follow_up_fee is None else float(doctor.Doctor.follow_up_fee)
                data['consultation_fee'] = 0 if doctor.Doctor.consultation_fee is None else float(doctor.Doctor.consultation_fee)
                data['biography'] = doctor.Doctor.biography
                data['medical_board_registrations'] = doctor.Doctor.medical_board_registrations
                data['know_languages'] = doctor.Doctor.know_languages
                data['status'] = doctor.Doctor.approved
                data['email'] = doctor.User.email
                data['image'] = doctor.Doctor.image
                data['contract_sign'] = doctor.Doctor.contract_sign
                data['notes'] = doctor.Doctor.notes

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error')#, 500
        finally:
            self.session.close()

    def getDoctorCenters(self, doctor_id):
        try:
            centers = self.session.query(CenetrDoctors, Center).filter(CenetrDoctors.doctor_id==doctor_id).all()
            
            result = []

            for center in centers:
                data = {}
                data['id'] = center.CenetrDoctors.id
                data['center_id'] = center.CenetrDoctors.center_id
                data['center'] = center.Center.name
                data['address'] = center.Center.address

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getCenterDoctors(self, id):
        try:
            doctors = self.session.query(CenetrDoctors, Doctor).filter(CenetrDoctors.center_id==id).all()
            
            result = []

            for doctor in doctors:
                data = {}
                data['id'] = doctor.CenetrDoctors.id
                data['center_id'] = doctor.CenetrDoctors.doctor_id
                data['first_name'] = doctor.Doctor.first_name
                data['last_name'] = doctor.Doctor.last_name
                data['user_id'] = doctor.Doctor.user_id
                data['speciality'] = doctor.Doctor.speciality

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()


    def updateDoctor(self, id, data):
        try:
            doctor = self.session.query(Doctor).filter(Doctor.id==id).first()

            doctor.first_name = data['first_name']
            doctor.last_name = data['last_name']
            doctor.gender = data['gender']
            doctor.birth_date = to_datetime(data['birth_date'])
            doctor.blood_type = data['blood_type']
            doctor.country = data['country']
            doctor.address = data['address']
            doctor.place_location = data['place_location']
            doctor.exact_location = data['exact_location']
            doctor.speciality = data['speciality']
            doctor.professional_experiance = data['professional_experiance']
            doctor.certification = data['certification']
            doctor.experiance = data['experiance']
            doctor.education = data['education']
            doctor.memberships = data['memberships']
            doctor.follow_up_fee = data['follow_up_fee']
            doctor.consultation_fee = data['consultation_fee']
            doctor.biography = data['biography']
            doctor.medical_board_registrations = data['medical_board_registrations']
            doctor.know_languages = data['know_languages']
            if 'contract_sign' in data:
                 doctor.contract_sign = not_exisit_in_request(data, 'contract_sign')
            doctor.notes = not_exisit_in_request(data, 'notes', doctor.notes)

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def updateImage(self, id, data):
        try:
            doctor = self.session.query(Doctor).filter(Doctor.user_id==id).first()

            doctor.image = data['image']

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def approveDoctor(self, id):
        try:
            doctor = self.session.query(Doctor).filter(Doctor.user_id==id).first()

            if doctor is None:
                return 'doctor not found', 404
            
            doctor.approved = 1
            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def disableDoctor(self, id):
        try:
            doctor = self.session.query(Doctor).filter(Doctor.user_id==id).first()

            if doctor is None:
                return 'doctor not found', 404
            
            doctor.approved = 0
            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def  joinHospital(self, doctor_id, center_id):
        try:
            center = self.session.query(Center).filter(Center.user_id==center_id).first()
            doctor = self.session.query(Doctor).filter(Doctor.user_id==doctor_id).first()

            if doctor is None or center is None:
                return 'not found', 404
            
            doctor.center.append(center)
            self.session.commit()

            return 'Ok', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    # get DoctorHistory by doctor_id
    def getDoctorHistory(self, doctor_id):
        try:
            # get doctor history with user data
            history = self.session.query(DoctorHistory, User).filter(DoctorHistory.doctor_id==doctor_id).filter(DoctorHistory.user_id==User.id).all()
             
            result = []

            for item, user in history:
                data = {}
                data['id'] = item.id
                data['doctor_id'] = item.doctor_id
                data['user_id'] = item.user_id
                data['username'] = item.username
                data['action'] = item.action
                data['action_timestamp'] = item.action_timestamp
                data['field_name'] = item.field_name
                data['old_value'] = item.old_value
                data['new_value'] = item.new_value

                result.append(data)

            return result, 200
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
    
    # get all DoctorHistory
    def getAllDoctorHistory(self):
        try:
            # get doctor history with user data and doctor data
            query = self.session.query(DoctorHistory, User, Doctor)
            query = query.filter(DoctorHistory.user_id==User.id)
            query = query.filter(DoctorHistory.doctor_id==Doctor.id)
            history = query.all()

            result = []

            for item, user, doctor in history:
                data = {}
                data['id'] = item.id
                data['doctor_id'] = item.doctor_id
                data['doctor'] = doctor.first_name + ' ' + doctor.last_name
                data['user_id'] = item.user_id
                data['username'] = item.username
                data['action'] = item.action
                data['action_timestamp'] = item.action_timestamp
                data['field_name'] = item.field_name
                data['old_value'] = item.old_value
                data['new_value'] = item.new_value

                result.append(data)

            return result, 200
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()