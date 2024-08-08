import jwt 

from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response, current_app
from werkzeug.security import check_password_hash
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.security.mail import confirm_token
from app.users.service import UserService
from .otp import get_user_otp, verify_OTP
from config import SecretKey
from datetime import datetime, timedelta


login = Blueprint('login', __name__)
SECRET_KEY = SecretKey().SECRET_KEY
service = UserService()

CORS(login, supports_credentials=True)

# login by both mbile or email
@login.route('/', methods=['GET', 'POST'])
@cross_origin()
def login_any():
    #auth = request.authorization
    data = request.json
    now = datetime.now()

    if not request.json or not 'username' in request.json or not 'password' in request.json:
        login_data = {'date': now, 'status': 'could not verify,  401', 'user_id': None}
        service.user_logins(login_data)
        return jsonify({'msg':'User name and password are required', 'status':401})

    # if not auth or not auth.username or not auth.password:
    #     login_data = {'date': now, 'status': 'could not verify,  401', 'user_id': None}
    #     service.user_logins(login_data)
    #     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = service.getUserByEmail(data["username"])

    if user is None:
        login_data = {'date': now, 'status': 'User not found, 404', 'user_id': None}
        service.user_logins(login_data)
        return jsonify({'msg':'User not found', 'status':404})


    if not user.User.active:
        login_data = {'date': now, 'status': 'User is not active,  401', 'user_id': user.User.id}
        service.user_logins(login_data)
        return jsonify({'msg':'User is not active!', 'status':401})

    if check_password_hash(user.User.password, data["password"]):
        login_data = {'date': now, 'status': 'ok,  200', 'user_id': user.User.id}
        service.user_logins(login_data)
        token = jwt.encode({'public_id': user.User.public_id, 'exp' : datetime.now() + timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
        return jsonify({'msg':'','token' : token, 'id' : user.User.id, 'role': user.Role.name, 'expiry' : datetime.now() + timedelta(hours=24),'has_profile': user.User.has_profile, 'active': user.User.active,'status':200}), 200
    
    return jsonify({'msg':'Wrong password', 'status':401})

@login.route('/admin', methods=['GET', 'POST'])
@cross_origin()
def login_admin():
    auth = request.json
    now = datetime.now()

    if not request.json or not 'username' in request.json or not 'password' in request.json:
        login_data = {'date': now, 'status': 'could not verify,  401', 'user_id': None}
        service.user_logins(login_data)

        return jsonify({'msg':'User name or password are required','status': 401})

    user = service.getUserAdmin(auth["username"])

    if user is None:
        login_data = {'date': now, 'status': 'User not found, 404', 'user_id': None}
        service.user_logins(login_data)
        return jsonify({'msg':'User not found' ,'status': 404})

    if not user.User.active:
        login_data = {'date': now, 'status': 'User is not active,  401', 'user_id': user.User.id}
        service.user_logins(login_data)
        return  jsonify({'msg':'User is not active!','status': 401})

    if check_password_hash(user.User.password, auth["password"]):
        login_data = {'date': now, 'status': 'ok,  200', 'user_id': user.User.id}
        service.user_logins(login_data)
        token = jwt.encode({'public_id': user.User.public_id, 'exp' : datetime.now() + timedelta(minutes=60)}, SECRET_KEY, "HS256")
        return jsonify({'msg':'','token' : token, 'id' : user.User.id, 'role': user.Role.name, 'role_id': user.Role.id, 'expiry' : datetime.now() + timedelta(minutes=60), 'email': user.User.email,'has_profile': user.User.has_profile, 'active': user.User.active,'status':200}), 200
    
    return jsonify({'msg':'Wrong password'},  401)

@login.route('/patient', methods=['GET', 'POST'])
@cross_origin()
def login_patient():
    auth = request.authorization

    response = make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    status = 'could not verify,  401'

    if not auth or not auth.username or not auth.password:
        status = 'could not verify,  401'
        response = make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = service.getUserByPhone(auth.username)

    if user.Role.name != 'Patient':
        status = 'could not verify Patient,  405'
        response =  make_response('could not verify Patient',  405, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.User.password, auth.password):
        token = jwt.encode({'public_id': user.User.public_id, 'exp' : datetime.utcnow() + timedelta(minutes=60)}, SECRET_KEY, "HS256")
        status = 'ok,  200'
        response = jsonify({'token' : token, 'id' : user.User.id}), 200

    #return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
    now = datetime.now()
    login_data = {'date': now, 'status': status, 'user_id': user.User.id}

    service.user_logins(login_data)
    return response

@login.route('/user', methods=['GET', 'POST'])
@cross_origin()
def login_user():
    auth = request.authorization

    response = make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    status = 'could not verify,  401'

    if not auth or not auth.username or not auth.password:
        status = 'could not verify,  401'
        response = make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = service.getUserByEmail(auth.username)

    if user.Role.name == 'Patient':
        status = 'could not verify User,  405'
        response = make_response('could not verify User',  405, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.User.password, auth.password):
        token = jwt.encode({'public_id': user.User.public_id, 'exp' : datetime.utcnow() + timedelta(minutes=60)}, SECRET_KEY, "HS256")
        status = 'ok,  200'
        response = jsonify({'token' : token, 'id' : user.User.id, 'has_profile' : user.User.has_profile}), 200

    #response = make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

    now = datetime.now()
    login_data = {'date': now, 'status': status, 'user_id': user.User.id}

    service.user_logins(login_data)
    return response

@login.route('/changepassword/<id>', methods=['GET', 'POST'])
@cross_origin()
def login_update_password(id):
    message, status = service.updateUserPassword(id, request.json)
    return jsonify({'msg': message, 'status':status}), status

@login.route('/resetpassword', methods=['POST'])
@cross_origin()
def login_reset_password():
    message, status = service.resetUserPassword(request.json)
    return jsonify({'msg': message, 'status':status}), status

@login.route('/forgotpassword/', methods=['POST'])
@cross_origin()
def login_forgot_password():
    message, status = service.forgetPassword(request.json)
    return jsonify({'msg': message, 'status':status}), status

## signup ##
signup = Blueprint('signup', __name__)

@signup.route('/', methods=['POST'])
@cross_origin()
def signup_user():
    if not request.json or not 'email' in request.json or not 'phone' in request.json:
         return jsonify({'msg':'email or phone are required', 'status':401})
    if not 'role' in request.json:
        return jsonify({'msg':'Role not found', 'status':404})

    response, status = service.createUser(request.json)
    return jsonify({'msg': response,'status':status}), status

## signup -> confirm ##
@signup.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify({'msg':'The confirmation link is invalid or has expired'},  201)
    
    message = service.user_confirmed(email)
    return jsonify({'msg':message, 'status':201},  201)

## signup -> send confirmation ##
@signup.route('/confirmation/', methods=['POST'])
@cross_origin()
def send_confirm_email():
    try:
        data = request.json
        email = data['email']
        if not request.json or not 'email' in request.json:
           return jsonify({'msg':'Email not found'},  404)
        user = service.getUserByEmail(email)
        if user is None:
           return jsonify({'msg':'User not found' ,'status': 404})
        service.send_confirmation_token(email)
        return jsonify({'msg':'The activation link has been sent via email'},  200)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({'msg':'Internal Server Error', 'status':500},  500)

## signup -> mobile verification ##
@signup.route('/mobile_otp/', methods=['POST'])
@cross_origin()
def mobile_otp():
    try:
        data = request.json
        country_code = data['country_code']
        phone_number = data['phone_number']
        

        user = service.getUserByMobile(phone_number)
        if user is None:
            return jsonify({'msg':'User Not Found'},  404)

        if user.active:
            return jsonify({'msg':'User is already verified'},  200)
        mobile = str(country_code) + str(phone_number)
        data.update({'email': user.email, 'mobile': mobile})
        token = get_user_otp(data)
        return jsonify({'token' : token}), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({'msg':'Internal Server Error'},  500)

@signup.route('/verify_mobile/', methods=['POST'])
@cross_origin()
def verify_mobile():
    try:
        # verify token
        verify, phone = verify_OTP(request.json)

        if verify:
            # update user
            message, status = service.user_confirmed_mobile(phone)
            return jsonify({'msg':message,  'status':status})

        return jsonify({'msg':'Cannot Verify User',  'status':400})        
    except Exception as e:
        current_app.logger.error(e)
        message = "{}".format(e)
        return jsonify({'msg':message,  'status':500})        

@login.route('/verify_otp', methods=['POST'])
@cross_origin()
def verify_otp():    
    message, status = service.verify_otp(request.json)
    return jsonify({'msg':message,  'status':status})

def check_token(token):
    try:
        # Decode the token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token, None
    except ExpiredSignatureError:
        return None, "Token has expired"
    except InvalidTokenError:
        return None, "Invalid token"

@login.route('/protected/', methods=['GET'])
def protected():
    token = request.headers.get('x-access-tokens')
    if not token:
        return jsonify({"message": "Token is missing", 'status':403}), 403

    # Remove 'Bearer ' from the token string if it's present
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]

    decoded_token, error = check_token(token)
    if error:
        return jsonify({"message": error, 'status':403}), 403

    # Token is valid, proceed with the protected resource
    return jsonify({"message": "Access granted", "data": decoded_token, 'status':200}), 200