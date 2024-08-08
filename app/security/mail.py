
from flask_mail import Mail, Message
from flask import Blueprint
from flask import current_app
from extensions import mail
from itsdangerous import URLSafeTimedSerializer

from config import SecretKey, MailConfig

SECRET_KEY = SecretKey().SECRET_KEY
SECURITY_PASSWORD_SALT = SecretKey().SECURITY_PASSWORD_SALT

def send_email(to, subject, template):
    try:
        if MailConfig().MAIL_ENABLED:
            #e_mail = Mail(current_app)

            msg = Message(
                subject,
                recipients=[to],
                html=template,
                sender=MailConfig().MAIL_DEFAULT_SENDER
            )
            mail.send(msg)
    except Exception as e:
        current_app.logger.info(current_app.config['MAIL_SERVER'])
        current_app.logger.info(current_app.config['MAIL_PORT'])
        current_app.logger.info(current_app.config['MAIL_USE_TLS'])
        current_app.logger.info(current_app.config['MAIL_USE_SSL'])
        current_app.logger.info(current_app.config['MAIL_USERNAME'])
        current_app.logger.info(current_app.config['MAIL_PASSWORD'])
        current_app.logger.error(e)

def send_email_bcc(to, subject, template):
    if MailConfig().MAIL_ENABLED:
        bcc = [MailConfig().ADMIN_EMAIL]

        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=MailConfig().MAIL_DEFAULT_SENDER,
            bcc=bcc
        )

        mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except Exception as e:
        current_app.logger.error(e)
        return False
    return email