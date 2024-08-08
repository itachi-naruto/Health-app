import os
from flask import current_app
from config import SMSConfig
from twilio.rest import Client

class twilio_service:
    def __init__(self):
        self.client = self.enable_sms()
    
    def enable_sms(self):
        try:
            # Your Account SID from twilio.com/console
            account_sid = SMSConfig().TWILIO_ACCOUNT_SID
            # Your Auth Token from twilio.com/console
            auth_token  = SMSConfig().TWILIO_AUTH_TOKEN

            self.client = None
            #if os.getenv('SMS_ENABLED'):
            self.client = Client(account_sid, auth_token)
        except Exception as e:
            current_app.logger.error(e)
        return self.client
    
    def send_sms(self,mobile, sms):
        try:
            message = self.client.messages.create(
                to=mobile, 
                from_=SMSConfig().TWILIO_MOBILE,
                body=sms)
            return message
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format(e), 500