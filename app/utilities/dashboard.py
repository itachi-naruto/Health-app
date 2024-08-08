## service layer of the API
import sqlalchemy as sql
from flask import current_app, Blueprint, jsonify
from app.security import roles
from datetime import datetime
from config import BaseConfig
from datetime import datetime, date
from sqlalchemy import or_, func
from flask_cors import CORS, cross_origin
from app.users.model import User, Role
from app.appointments.model import Appointment
from app.status.model import Status
from app.doctors.model import Doctor
from app.payment_transaction.model import PaymentTransaction

## dashboard ##
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET'])
@cross_origin()
@roles.token_required
def get_statistics_route(self):
    dasboard_instance = Dasboard()
    return dasboard_instance.getStatistics()

@dashboard.route('/payment', methods=['GET'])
@cross_origin()
def get_payment():
    dasboard_instance = Dasboard()
    return dasboard_instance.getAllPaymentTransactions()

@dashboard.route('/appointment', methods=['GET'])
@cross_origin()
def get_appointment():
    dasboard_instance = Dasboard()
    return dasboard_instance.getAppointment()

class Dasboard:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()



    def getStatistics(self):
        try:
            role_counts = self.session.query(
                Role.name,
                func.count(User.id)
            ).join(User.roles).filter(
                or_(Role.name == 'Doctor', Role.name == 'Center', Role.name == 'Patient'),
                User.active == 1
            ).group_by(Role.name).all()


            # Convert role_counts query result to a dictionary
            role_counts_dict = {role: count for role, count in role_counts}
            
            # Query to get the total number of active users
            total_active_users = sum(role_counts_dict.values())
            role_counts_dict['total_active_users'] = total_active_users
        
           # Query to count the number of users for each appointment
            appointment_counts = self.session.query(
                Status.name,
                func.count(Appointment.id)
            ).join(Appointment, Appointment.status_id == Status.id).filter(
                or_(Status.name == 'Book', Status.name == 'Confirm', Status.name == 'Done')
            ).group_by(Status.name).all()

            # Convert appointment_counts query result to a dictionary
            appointment_counts_dict = {status: count for status, count in appointment_counts}
            
            # Query to get the total number of all appointments
            total_appointments = sum(appointment_counts_dict.values())

            # Add total appointment count to the result
            appointment_counts_dict['total_appointment'] = total_appointments

            # Query to get the total number of transactions
            total_transactions = self.session.query(
                func.count(PaymentTransaction.id)
            ).scalar()

            # Query to get the number of transactions made today
            today = datetime.today()
            today_transactions = self.session.query(
                func.count(PaymentTransaction.id)
            ).filter(
                func.date(PaymentTransaction.create_date) == today
            ).scalar()
           
            transactions_dict = {
                "total_transactions": total_transactions,
                "today_transactions": today_transactions
            }
          # Create the response dictionary
            response_dict = {
                "registered": role_counts_dict,
                "appointments": appointment_counts_dict,
                "payments": transactions_dict
               
            }
            return jsonify(response_dict), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            self.session.close()
   
   
    def getAppointment(self):
        try:
            # Query to count the number of users for each appointment
            appointment_counts = self.session.query(
                Status.name,
                func.count(Appointment.id)
            ).join(Appointment, Appointment.status_id == Status.id).filter(
                or_(Status.name == 'Book', Status.name == 'Confirm', Status.name == 'Done')
            ).group_by(Status.name).all()

            # Convert appointment_counts query result to a dictionary
            appointment_counts_dict = {status: count for status, count in appointment_counts}
            
            # Query to get the total number of all appointments
            total_appointments = sum(appointment_counts_dict.values())

            # Add total appointment count to the result
            appointment_counts_dict['total_appointment'] = total_appointments

            return jsonify(appointment_counts_dict), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            self.session.close()



    def getAllPaymentTransactions(self):
        try:
            # Query to get the total number of transactions
            total_transactions = self.session.query(
                func.count(PaymentTransaction.id)
            ).scalar()

            # Query to get the number of transactions made today
            today = datetime.today()
            today_transactions = self.session.query(
                func.count(PaymentTransaction.id)
            ).filter(
                func.date(PaymentTransaction.create_date) == today
            ).scalar()

            # Query to get all transaction details
            all_transactions = self.session.query(PaymentTransaction).all()

            # Convert all transactions to a list of dictionaries
            transactions_list = [
                {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "date": transaction.create_date,
                    "status": transaction.active
                    # Add other necessary fields here
                } for transaction in all_transactions
            ]

            # Create the response dictionary
            response_dict = {
                "total_transactions": total_transactions,
                "today_transactions": today_transactions,
                "all_transactions": transactions_list
            }

            return jsonify(response_dict), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            self.session.close()

    def getNextScheduel(self, id):
        try:
            schedule = self.session.query(Doctor).filter(Doctor.date_time >= datetime.today()).filter(Doctor.active==1).filter(Doctor.doctor_id==id).order_by(Doctor.date_time.asc()).first()
            
            return schedule.date_time if schedule is not None else ''
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()
