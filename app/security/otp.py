import math, random
import jwt 
import datetime
from config import SecretKey
from flask import render_template
from .mail import send_email
from app.sms.twilio import twilio_service

SECRET_KEY = SecretKey().SECRET_KEY

def get_user_otp(data):
	otp = generate_otp()
	# send OTP by SMS => data[county_code], data[phone_number]
	# send email for testing
	message = 'Please use OTP number ({0}) to complete the mobile verification, this OTP expires in 5 minutes.'.format(otp)
	html = render_template('email.html', message=message)
	subject = "Please Verify Your Mobile Number."

	twilio_service().send_sms(data['mobile'], message)
	send_email(data['email'], subject, html)
	#print(otp)

	# generate token of OTP 
	token = jwt.encode({'mobile': data['phone_number'], 'otp': otp, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, SECRET_KEY, "HS256")

	return token

def generate_otp():
	digits = "0123456789"
	OTP = ''

    # for a 4 digit OTP we are using 4 in range
	for i in range(4) : 
		OTP += digits[math.floor(random.random() * 10)] 

	return OTP

def verify_OTP(data):
	phone_number = data['phone_number']
	OTP = data['otp']
	token = data['token']

	payload = jwt.decode(token, SECRET_KEY, "HS256")

	if int(phone_number) == int(payload['mobile']) and int(OTP) == int(payload['otp']):
		return True, phone_number
	return False, phone_number