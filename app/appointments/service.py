## service layer of the API
import json
import sqlalchemy as sql
from sqlalchemy import func, extract, case
from flask import render_template,current_app
from datetime import datetime, date
from sqlalchemy.orm.query import Query
from config import BaseConfig
from .model import Appointment
from sqlalchemy import or_, and_
from app.utilities.request_utils import to_datetime
from app.security.mail import send_email
from app.doctors.model import Doctor
from app.centers.model import Center
from app.patients.model import Patient
from app.status.model import Status
from app.users.model import User
from app.schedules.model import Schedule

class AppointmentService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getAppointments(self, id): 
        try:
            query = self.session.query(Appointment, Doctor, Patient, Status, Center)
            query = query.join(Center, Center.id==Appointment.center_id, isouter=True)
            query = query.filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id)

            if id is None:
                appointments = query.all()
            else:
                appointments = query.filter(Appointment.id==id).all()

            # if id is None:
            #     appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).all()
            # else:
            #     appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(Appointment.id==id).all()
            
            result = []

            for appointment in appointments:
                data = {}
                data['id'] = appointment.Appointment.id
                data['date'] = appointment.Appointment.date
                data['update_date'] = appointment.Appointment.update_date
                data['period'] = appointment.Appointment.period
                data['doctor_id'] = appointment.Appointment.doctor_id
                data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                data['center_id'] = appointment.Appointment.center_id
                data['center'] = 'Online' if appointment.Center is None else appointment.Center.name
                data['patient_id'] = appointment.Appointment.patient_id
                data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                data['status_id'] = appointment.Appointment.status_id
                data['status'] = appointment.Status.name
                data['payment_id'] = appointment.Appointment.payment_id
                data['slot_id'] = appointment.Appointment.slot_id
                
                result.append(data)

            return result, 200
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
  
    def getDoctorAppointments(self, id): 
        try:
            appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(and_(Appointment.status_id!=8,Appointment.status_id!=9)).filter(Appointment.doctor_id==id).all()
            
            result = []

            for appointment in appointments:
                data = {}
                data['id'] = appointment.Appointment.id
                data['date'] = appointment.Appointment.date
                data['update_date'] = appointment.Appointment.update_date
                data['period'] = appointment.Appointment.period
                data['doctor_id'] = appointment.Appointment.doctor_id
                data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                data['center_id'] = appointment.Appointment.center_id
                data['center'] = 'Online' if appointment.Center is None else appointment.Center.name
                data['patient_id'] = appointment.Appointment.patient_id
                data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                data['status_id'] = appointment.Appointment.status_id
                data['status'] = appointment.Status.name
                data['payment_id'] = appointment.Appointment.payment_id
                data['symptoms'] = appointment.Appointment.symptoms
                data['date_of_birth'] = appointment.Patient.birth_date
                data['gender'] = appointment.Patient.gender
                data['blood_type'] = appointment.Patient.blood_type.upper()
                data['contact_number'] = self.getContactNumber(appointment.Patient.user_id, appointment.Patient.parent_id)
                data['country'] = appointment.Patient.country
                data['slot_id'] = appointment.Appointment.slot_id
                data['dr_user_id'] = appointment.Doctor.user_id

                today = date.today()
                dob = appointment.Patient.birth_date
                age = today.year - dob.year

                data['age'] = age

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getDoctorPatients(self, id): 
        try:
            appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(Appointment.status_id==9).filter(Appointment.doctor_id==id).all()
            
            result = []

            for appointment in appointments:
                data = {}
                data['id'] = appointment.Appointment.id
                data['date'] = appointment.Appointment.date
                data['update_date'] = appointment.Appointment.update_date
                data['period'] = appointment.Appointment.period
                data['doctor_id'] = appointment.Appointment.doctor_id
                data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                data['center_id'] = appointment.Appointment.center_id
                data['center'] = 'Online' if appointment.Center is None else appointment.Center.name
                data['patient_id'] = appointment.Appointment.patient_id
                data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                data['status_id'] = appointment.Appointment.status_id
                data['status'] = appointment.Status.name
                data['payment_id'] = appointment.Appointment.payment_id
                data['symptoms'] = appointment.Appointment.symptoms
                data['date_of_birth'] = appointment.Patient.birth_date
                data['gender'] = appointment.Patient.gender
                data['blood_type'] = appointment.Patient.blood_type.upper()
                data['contact_number'] = self.getContactNumber(appointment.Patient.user_id, appointment.Patient.parent_id)
                data['country'] = appointment.Patient.country
                data['slot_id'] = appointment.Appointment.slot_id
                data['dr_user_id'] = appointment.Doctor.user_id

                today = date.today()
                dob = appointment.Patient.birth_date
                age = today.year - dob.year

                data['age'] = age

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getPatientAppointments(self, id): 
        try:
            appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(Appointment.patient_id==id).order_by(and_(Appointment.status_id, Appointment.date)).all()
            
            result = []

            for appointment in appointments:
                data = {}
                data['id'] = appointment.Appointment.id
                data['date'] = appointment.Appointment.date
                data['update_date'] = appointment.Appointment.update_date
                data['period'] = appointment.Appointment.period
                data['dr_user_id'] = appointment.Doctor.user_id
                data['doctor_id'] = appointment.Appointment.doctor_id
                data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                data['center_id'] = appointment.Appointment.center_id
                data['center'] = '{0} {1}'.format(appointment.Doctor.place_location, appointment.Doctor.exact_location) if appointment.Center is None else appointment.Center.name
                data['patient_id'] = appointment.Appointment.patient_id
                data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                data['status_id'] = appointment.Appointment.status_id
                data['status'] = appointment.Status.name
                data['payment_id'] = appointment.Appointment.payment_id
                data['symptoms'] = appointment.Appointment.symptoms
                data['slot_id'] = appointment.Appointment.slot_id

                result.append(data)
                
            patients = self.session.query(Patient).filter(Patient.parent_id==id).all()
            if patients is not None:
                for p in patients:
                    p_appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(Appointment.patient_id==p.id).all() 

                    for appointment in p_appointments:
                        data = {}
                        data['id'] = appointment.Appointment.id
                        data['date'] = appointment.Appointment.date
                        data['update_date'] = appointment.Appointment.update_date
                        data['period'] = appointment.Appointment.period
                        data['doctor_id'] = appointment.Appointment.doctor_id
                        data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                        data['center_id'] = appointment.Appointment.center_id
                        data['center'] = '{0} {1}'.format(appointment.Doctor.place_location, appointment.Doctor.exact_location) if appointment.Center is None else appointment.Center.name
                        data['patient_id'] = appointment.Appointment.patient_id
                        data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                        data['status_id'] = appointment.Appointment.status_id
                        data['status'] = appointment.Status.name
                        data['payment_id'] = appointment.Appointment.payment_id
                        data['symptoms'] = appointment.Appointment.symptoms
                        data['slot_id'] = appointment.Appointment.slot_id

                        result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getCenterAppointments(self, id): 
        try:
            appointments = self.session.query(Appointment, Doctor, Patient, Status, Center).join(Center, Center.id==Appointment.center_id, isouter=True).filter(Appointment.doctor_id==Doctor.id, Appointment.patient_id==Patient.id, Appointment.status_id==Status.id).filter(Appointment.center_id==id).all()
            
            result = []

            for appointment in appointments:
                data = {}
                data['id'] = appointment.Appointment.id
                data['date'] = appointment.Appointment.date
                data['update_date'] = appointment.Appointment.update_date
                data['period'] = appointment.Appointment.period
                data['doctor_id'] = appointment.Appointment.doctor_id
                data['doctor'] = appointment.Doctor.first_name + ' ' + appointment.Doctor.last_name
                data['center_id'] = appointment.Appointment.center_id
                data['center'] = 'Online' if appointment.Center is None else appointment.Center.name
                data['patient_id'] = appointment.Appointment.patient_id
                data['patient'] = appointment.Patient.first_name + ' ' + appointment.Patient.last_name
                data['status_id'] = appointment.Appointment.status_id
                data['status'] = appointment.Status.name
                data['payment_id'] = appointment.Appointment.payment_id
                data['symptoms'] = appointment.Appointment.symptoms
                data['slot_id'] = appointment.Appointment.slot_id

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def createAppointment(self, data):
        try:
            appointment = Appointment(
            date=to_datetime(data['date']),
            period=data['period'],
            doctor_id=data['doctor_id'],
            center_id=data['center_id'],
            patient_id=data['patient_id'],
            symptoms=data['symptoms'],
            slot_id=data['slot_id'] if data['slot_id'] is not None else 0,
            status_id=4)

            self.session.add(appointment)
            self.session.commit()

            if appointment: 
                try:
                    user = self.session.query(User.email).filter(Patient.user_id==User.id).filter(Patient.id==data['patient_id']).first()
                    message = 'Your appointment has been created, Your appointment will confirmed once payment is completed.'
                    html = render_template('email.html', message=message)
                    subject = 'Appointment {}'.format(appointment.id)
                    send_email(user.email, subject, html)
                except Exception as e:
                    current_app.logger.error(e)

            return appointment.id, 201
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
    
    def updateAppointmentStatus(self, id, status_id):
        try:
            appointment = self.session.query(Appointment).filter(Appointment.id==id).first()

            appointment.update_date = datetime.now()
            appointment.status_id = status_id

            """ if status_id == 6 or status_id == 7: 
                appointment.date = data['date']
                appointment.period = data['period'] """

            self.session.commit()

            try:
                user = self.session.query(User.email).filter(Patient.user_id==User.id).filter(Patient.id==appointment.patient_id).first()
                status = self.session.query(Status.name).filter(Status.id==status_id).first()
                message = 'Your appointment has been {} on {}. Please check with your doctor.'.format(status.name, datetime.now().strftime("%c"))
                html = render_template('email.html', message=message)
                subject = 'Appointment {}'.format(appointment.id)
                send_email(user.email, subject, html)
                return message, 200
            except Exception as e:
                current_app.logger.error(e)

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def updateAppointment(self, id, data):
        try:
            appointment = self.session.query(Appointment).filter(Appointment.id==id).first()

            appointment.date = data['date']
            appointment.period = data['period']
            appointment.doctor_id = data['doctor_id']
            appointment.center_id = data['center_id']
            appointment.patient_id = data['patient_id']
            appointment.status_id = data['status_id']
            appointment.slot_id=data['slot_id']
            appointment.symptoms = data['symptoms'] if data['symptoms'] is not None else ''

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def deleteAppointment(self, id, unbook):
        try:
            appointment = self.session.query(Appointment).filter(Appointment.id==id).first()

            if appointment == None:
                return 'Not Found', 404
            
            if appointment and unbook:
                schedule = self.session.query(Schedule).filter(Schedule.id==appointment.slot_id).first()
                schedule.active = 1
                self.session.commit()

            self.session.delete(appointment)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getContactNumber(self, user_id, parent_id) :
        try:
            user = self.session.query(User).filter(User.id==user_id).first()
            
            if user is None: 
                user = self.session.query(User, Patient).filter(User.id==Patient.user_id).filter(Patient.parent_id==parent_id).first()
                return user.User.phone

            return user.phone
        except Exception as e:
            return 500
        finally:
            self.session.close()

    def updateAppointmentPayment(self, id, payment_id):
        try:
            appointment = self.session.query(Appointment).filter(Appointment.id==id).first()
            appointment.payment_id = payment_id

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
        finally:
            self.session.close()