## service layer of the API
import json
import sqlalchemy as sql
from flask import current_app
from sqlalchemy.orm.query import Query
from config import BaseConfig
from app.utilities.request_utils import to_datetime

from app.users.model import User
from .model import Patient

class PatientService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getPatients(self, id): 
        try:
            if id is None:
                patients = self.session.query(Patient, User).filter(Patient.parent_id==None).filter(Patient.user_id==User.id).all()
            else:
                patients = self.session.query(Patient, User).filter(Patient.parent_id==None).filter(Patient.user_id==User.id).filter(Patient.user_id==id).all()
            
            result = []

            for patient in patients:
                data = {}
                data['id'] = patient.Patient.user_id
                data['patient_id'] = patient.Patient.id
                data['first_name'] = patient.Patient.first_name
                data['last_name'] = patient.Patient.last_name
                data['civil_id'] = patient.Patient.civil_id
                data['address'] = patient.Patient.address
                data['gender'] = patient.Patient.gender
                data['birth_date'] = patient.Patient.birth_date
                 # Check if the blood_type attribute exists before converting to uppercase
                if hasattr(patient.Patient, 'blood_type') and patient.Patient.blood_type:
                    data['blood_type'] = patient.Patient.blood_type.upper()
                else:
                    data['blood_type'] = None
               
                data['country'] = patient.Patient.country
                data['email'] = patient.User.email
                data['phone'] = patient.User.phone

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def updatePatient(self, id, data):
        try:
            patient = self.session.query(Patient).filter(Patient.user_id==id).first()

            patient.first_name = data['first_name']
            patient.last_name = data['last_name']
            patient.civil_id = data['civil_id']
            patient.address = data['address']
            patient.gender = data['gender']
            patient.birth_date = to_datetime(data['birth_date'])
            patient.blood_type = data['blood_type']
            patient.country = data['country']

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    # add Patient 
    def add_patient(self, data):
        try:
            if not data or not 'civil_id' in data:
              return 'civil id is required', 401
            
            if not data or not 'first_name' in data:
              return 'First name is required', 401
            
            if not data or not 'gender' in data:
              return 'Gender is required', 401
            
            if not data or not 'blood_type' in data:
              return 'Blood type is required', 401
          
            if not data or not 'user_id' in data:
              return 'user is required', 401
    
            user = self.session.query(User).filter(User.id == data['user_id']).first()
            if user is None:
               return 'User not found',  404
                        
            user_doctor = self.session.query(Patient).filter(Patient.user_id == data['user_id']).first()
            if user_doctor:
               return 'The patient already has a profile.',  200
            
            patient = Patient(first_name=data['first_name'], 
                            last_name=data['last_name'],
                            civil_id=data['civil_id'],
                            address=data['address'],
                            gender=data['gender'],
                            user_id=data['user_id'],
                            birth_date=to_datetime(data['birth_date']),
                            blood_type=data['blood_type'],
                            country=data['country'])
            self.session.add(patient)
            self.session.commit()
            if patient:
                   return "Patient is Created", 201

        except Exception as e:
            current_app.logger.error(e)
            self.session.rollback()
            return "{}".format("Internal Server Error"), 500
        finally:
            self.session.close()
        
    # dependens actions
    def add_dependent(self, id, data):
        try:
            dependent = Patient(first_name=data['first_name'], 
                          last_name=data['last_name'],
                          gender=data['gender'],
                          birth_date=data['birth_date'],
                          blood_type=data['blood_type'],
                          relation=data['relation'])
            
            patient = self.session.query(Patient).filter(Patient.id==id).first()
            patient.dependents.append(dependent)

            self.session.commit()

            return 'Ok', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()


    def get_dependents(self, parent_id, patinet_id):
        try:
            if patinet_id is None:
                patients = self.session.query(Patient).filter(Patient.parent_id==parent_id).all()
            else:
                patients = self.session.query(Patient).filter(Patient.parent_id==parent_id).filter(Patient.id==patinet_id).all()
            
            result = []

            for patient in patients:
                data = {}
                data['patient_id'] = patient.id
                data['first_name'] = patient.first_name
                data['last_name'] = patient.last_name
                data['gender'] = patient.gender
                data['birth_date'] = patient.birth_date
                data['blood_type'] = patient.blood_type.upper()
                data['parent_id'] = patient.parent_id
                data['relation'] = patient.relation

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def update_dependent(self, id, data):
        try:
            patient = self.session.query(Patient).filter(Patient.id==id).first()

            patient.first_name = data['first_name']
            patient.last_name = data['last_name']
            patient.gender = data['gender']
            patient.birth_date = data['birth_date']
            patient.blood_type = data['blood_type']
            patient.relation = data['relation']

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def delete_dependent(self, id):
        try:
            dependet = self.session.query(Patient).filter(Patient.id==id).first()

            if dependet == None:
                return 'Not Found', 404
            
            self.session.delete(dependet)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()