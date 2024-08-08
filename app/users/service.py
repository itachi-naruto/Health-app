import json
import sqlalchemy as sql
import base64, uuid 
import string

from flask import url_for, render_template, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.query import Query
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

from app.utilities.request_utils import to_datetime
from .model import User, Role, Tracking
from config import BaseConfig
from app.patients.model import Patient
from app.doctors.model import Doctor
from app.centers.model import Center
from app.security.mail import confirm_token, generate_confirmation_token, send_email
from random import randint
from datetime import datetime, timedelta

class UserService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

     # create (sing-up) new user
    def createUser(self, data):
        try:
            # check if user is already exist
            
            #check_user = self.session.query(User).filter(or_(User.email==data['email'], User.phone==data['phone'])).first()
            #if check_user:
            #    return "user is already exist", 400
            check_email = self.session.query(User).filter(User.email == data['email']).first()
            check_phone = self.session.query(User).filter(User.phone == data['phone']).first()

            if check_email or check_phone:
                return "user is already exist", 400
            
            hash_pass = generate_password_hash(data['password'], method=BaseConfig.HASH_METHOD)
            user = User(public_id=str(uuid.uuid4()), 
                        password=hash_pass, 
                        email=data['email'], 
                        phone=data['phone'],
                        active=0)

            role_type = data['role']
            role = self.session.query(Role).filter(Role.name==role_type).first()

            user.roles.append(role)

            # if role_type == 'Patient':
            #     patient = self.add_patient(data)
            #     user.patients.append(patient)

            # if role_type == 'Doctor':
            #     doctor = self.add_doctor(data)
            #     user.doctors.append(doctor)

            # if role_type == 'Center':
            #     center = self.add_center(data)
            #     user.centers.append(center)

            self.session.add(user)
            self.session.commit()

            ## email confirmation goes here ##
            ## if user and role_type in [Doctor, Center] = send email verfication 
            ## patient will have to do OTP SMS verification 
            if user:
                try:
                    token = generate_confirmation_token(user.email)
                    confirm_url = url_for('signup.confirm_email', token=token, _external=True)
                    html = render_template('activate.html', confirm_url=confirm_url)
                    subject = "[Dr Search] Please Verify Your Email Address."
                    send_email(user.email, subject, html)
                except Exception as e:
                    current_app.logger.error(e)
                    return "User is Created", 201

            return "Confirmation Email Sent", 200
        except Exception as e:
            current_app.logger.error(e)
            self.session.rollback()
            return "{}".format("Internal Server Error"), 500
        finally:
            self.session.close()


    # add doctor model
    def add_doctor(self, data):
        try:
            _doctor = Doctor(first_name=data['first_name'], 
                            last_name=data['last_name'],
                            gender=data['gender'],
                            birth_date=to_datetime(data['birth_date']),
                            blood_type=data['blood_type'],
                            country=data['country'],
                            address=data['address'],
                            place_location=data['place_location'],
                            exact_location=data['exact_location'],
                            speciality=data['speciality'],
                            professional_experiance= '' if data['professional_experiance'] is None else  data['professional_experiance'],
                            certification=data['certification'],
                            experiance=data['experiance'],
                            education=data['education'],
                            memberships=data['memberships'],
                            follow_up_fee=data['follow_up_fee'],
                            consultation_fee=data['consultation_fee'],
                            biography=data['biography'],
                            medical_board_registrations=data['medical_board_registrations'],
                            know_languages=data['know_languages'])
            return _doctor
        except Exception as e:
            current_app.logger.error(e)
            return None

    # add medical center model
    def add_center(self, data):
        try:
            _center = Center(name=data['name'], 
                        country=data['country'],
                        address=data['address'],
                        place_location=data['place_location'],
                        exact_location=data['exact_location'],
                        longitude=data['longitude'],
                        latitude=data['latitude'],
                        speciality='',
                        description='',
                        start='',
                        end='',
                        image='',
                        #departments=[],
                        #schedule='',
                        center_type=data['center_type'])
            
            return _center
        except Exception as e:
            current_app.logger.error(e)
            return None

    def getUsers(self):
        try:
            users = self.session.query(User).all()
            result = []  

            for user in users:
                user_data = {}   
                user_data['id'] = user.id
                user_data['is_active'] = user.active
                user_data['phone'] = user.phone
                user_data['email'] = user.email
                user_data['mobile_confirmed_at'] = user.mobile_confirmed_at
                user_data['email_confirmed_at'] = user.email_confirmed_at
                user_data['roles'] = [role.name for role in user.roles]
                user_data['status'] = 200
                
                result.append(user_data)

            return result
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    # get user by mobile
    def getUserByMobile(self, mobile):
        try:
            user = self.session.query(User).filter(User.phone==mobile).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    # get user by email
    def getUserByEmail(self, email):
        try:
            user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.email==email).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    # get user by email
    def getUserAdmin(self, email):
        try:
            user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.email==email).filter(or_(Role.name=='Admin', Role.name=='Manager')).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()
    
    # get user by phone  or email
    def getUserByAny(self, param):
        try:
            user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(or_(User.email==param, User.phone==param)).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    # get user by UUID
    def getUserByPublicID(self, public_id) :
        try:
            user = self.session.query(User).filter(User.public_id==public_id).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    def get_user_by_id(self, id):
        try:
            user_row = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.id == id).first()

            if not user_row:
                return "User not found", 404

            user = user_row.User

            user_dict = {
                "id": user.id,
                "is_active": user.active,
                "phone": user.phone,
                "email": user.email,
                "roles":user_row.Role.name,
                "msg":'',
                "status":200
            }

            return user_dict, 200

        except Exception as e:
            return  str(e), 500

        finally:
            self.session.close()
    
    def getUserByID(self, id) :
        try:
            user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.id==id).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    # get username by UUID
    def getUsernameByPublicID(self, public_id) :
        try:
            user = None
            user = self.session.query((Doctor.first_name).label('first_name'), (Doctor.last_name).label('last_name')).filter(User.public_id==public_id).filter(User.id==Doctor.user_id).first()

            if user is None:
                user = self.session.query((Patient.first_name).label('first_name'), (Patient.last_name).label('last_name')).filter(User.public_id==public_id).filter(User.id==Patient.user_id).first()
            
            if user is None:
                return None

            return '{} {}'.format(user.first_name, user.last_name)
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    def getUserByPublicIDWithRole(self, public_id) :
        try:
            user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.public_id==public_id).first()
            return user
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    # log user logins
    def user_logins(self, data):
        try:
            track = Tracking(date=data['date'],status=data['status'],user_id=data['user_id'])
           
            self.session.add(track)
            self.session.commit()

            return "ok", 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    # confirm user signup / registration
    def user_confirmed(self, email):
        try:
            user = self.session.query(User).filter(User.email==email).first()

            if user.active:
                return 'Account already confirmed. Please login.'
            else:
                user.active = True
                user.email_confirmed_at = datetime.now()
                self.session.add(user)
                self.session.commit()
                return 'You have confirmed your account. Thanks!'
        except Exception as e:
            self.session.rollback()
            print("user email confirmation error {}".format(e))
            return "The confirmation link is invalid."
        finally:
            self.session.close()

    def user_confirmed_mobile(self, phone):
        try:
            user = self.session.query(User).filter(User.phone==phone).first()
            
            if user.active:
                return 'Account already confirmed. Please login.', 200

            user.active = True
            user.mobile_confirmed_at = datetime.now()
            self.session.add(user)
            self.session.commit()

            return 'Mobile Confirmation Updated!', 200
        except Exception as e:
            self.session.rollback()
            print("Mobile confirmation error {}".format(e))
            return "Internal Server Error", 500
        finally:
            self.session.close()

    # reset password
    def resetUserPassword(self, data): 
        try:

            if not data or not 'password' in data:

                return 'password is required', 401
            if not data or not 'email' in data:

                return 'Email is required', 401

            user = self.session.query(User).filter(User.email == data["email"]).first()
            if user is None:

                return 'User not found',  404

            if not user.active:
                return  'User is not active!',  401

            hash_password = generate_password_hash(data["password"], method=BaseConfig.HASH_METHOD)
            
            user.password = hash_password
            self.session.commit()
            return "password updated", 200
         
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def updateUserPassword(self, id, data): 
        try:

            if not data or not 'new_password' in data or not 'password' in data:

                return 'Old and new password are required', 401

            user = self.session.query(User).filter(User.id == id).first()
            if user is None:

                return 'User not found',  404

            if not user.active:
                return  'User is not active!',  401

            if check_password_hash(user.password, data["password"]):

                   hash_password = generate_password_hash(data["new_password"], method=BaseConfig.HASH_METHOD)
                   
                   user.password = hash_password
                   self.session.commit()
                   return "password updated", 200
            
            return 'could not verify',  401
         
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def forgetPassword(self, data):
        try:
            if not data or not 'email' in data:

              return 'Email is required', 401

            user = self.session.query(User).filter(User.email==data['email']).first()
            if user is None:

                return 'User not found',  404
            # password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # hash_password = generate_password_hash(password, method=BaseConfig.HASH_METHOD)

            otp = randint(1000, 9999)  # Generate a 4-digit OTP
            expiration_time = datetime.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
            # return expiration_time, 200
            user.otp = otp
            user.expiration_time = expiration_time
            
            self.session.commit()

            html = render_template('forget.html',otp=otp)
            subject = "[Dr Search] Your OTP Code."
            send_email(user.email, subject, html)

            return "The otp has been sent via email.", 200
        except Exception as e:
            print("forgot password error: {}".format(e))
            self.session.rollback()
            return "error prcessing request", 500
        finally:
            self.session.close()

    def deleteUser(self, id):
        try:
            user = self.session.query(User).filter(User.id==id).first()

            if user == None:
                return 'Not Found', 404
            
            self.session.delete(user)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    
    def disableUser(self, id):
        try:
            user = self.session.query(User).filter(User.id==id).first()

            if user is None:
                return 'user not found', 404
            
            user.active = 0
            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def enableUser(self, id):
        try:
            user = self.session.query(User).filter(User.id==id).first()

            if user is None:
                return 'user not found', 404
            
            user.active = 1
            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def getRoles(self):
        try:
            roles = self.session.query(Role).all()
            result = []  

            for role in roles:
                data = {}   
                data['id'] = role.id
                data['name'] = role.name
                
                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
   
    def send_confirmation_token(self, email):
        
        user = self.session.query(User, Role).join(User.roles).options(joinedload(User.roles)).filter(User.email==email).first()

        if user is None:
            return 'User not found',  404

        if user.User.active:
            return  'User is already active!',  200
        
        token = generate_confirmation_token(email)
        confirm_url = url_for('signup.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "[Dr Search] Please Verify Your Email Address."
        send_email(email, subject, html)
    def verify_otp(self, data):
        
        # Retrieve stored OTP and expiration time from your database
        try:

            if not data or not 'otp' in data or not 'email' in data:

                return 'otp or email is required', 401

            user = self.session.query(User).filter(User.email == data['email']).first()
            if user is None:
                return 'User not found',  404

            if datetime.now() > user.expiration_time:
                return  "OTP has expired.", 401

            if data['otp'] != user.otp:
                return "Invalid OTP.", 401

            return "OTP verified successfully.",  200
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    def showLogins(self):
        try:
            logins = self.session.query(Tracking, User).filter(User.id==Tracking.user_id).order_by(Tracking.date.desc()).limit(100).all()
            result = []  

            for login in logins:
                data = {}   
                data['id'] = login.Tracking.id
                data['date'] = login.Tracking.date
                data['status'] = login.Tracking.status
                data['others'] = login.Tracking.others
                data['user_id'] = login.Tracking.user_id
                data['user_email'] = login.User.email
                
                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()