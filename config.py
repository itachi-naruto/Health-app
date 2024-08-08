import os
import sqlalchemy as sql
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config:
    """Configuration from environment variables."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    FLASK_APP = 'app.py'
class BaseConfig(object):
    DEBUG = os.getenv('DEBUG','True')
    HASH_METHOD = os.getenv('HASH_METHOD','scrypt')
    HOST_URL = os.getenv('HOST_URL','http://localhost:8000')
    #DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///api.sqlite3')
    DATABASE_URL = ''
    DB_TYPE = os.getenv('DB_TYPE','sqlite')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE_NAME = os.getenv('DB_DATABASE_NAME')
    DB_CONNECTION_NAME = os.getenv('DB_CONNECTION_NAME')
    DB_HOST = os.getenv('DB_HOST','127.0.0.1:3306')
    UPLOAD_FOLDER = 'uploads/'

    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.getenv('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(DB_CONNECTION_NAME)
        DATABASE_URL = 'mysql+pymysql://{}:{}@/{}?unix_socket={}'.format(
            DB_USERNAME, DB_PASSWORD, DB_DATABASE_NAME, unix_socket)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        #host = '127.0.0.1'
        if DB_TYPE == 'sqlite':
            DATABASE_URL = 'sqlite:///{}.sqlite3'.format(DB_DATABASE_NAME)

        else:
            DATABASE_URL = 'mysql+pymysql://{}:{}@{}/{}'.format(
                DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE_NAME)

    engine = sql.create_engine('%s'%DATABASE_URL, pool_pre_ping=True, pool_recycle=2600)
    #engine = sql.create_engine('mysql+mysqlconnector://smartlab_amjadizz:amjadizz@localhost:3306/smartlab_amjadizz', pool_pre_ping=True, pool_recycle=2600)

class SecretKey(object):
    DEBUG = os.getenv('DEBUG','True')
    SECRET_KEY = os.getenv('SECRET_KEY','_P@ssw0rd_1')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT','password_@dr_search968')

class SMSConfig(object):
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID','')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN','')
    TWILIO_MOBILE = os.getenv('TWILIO_MOBILE','')
class FileUploadConfig(object):
    STORAGE = os.getenv('STORAGE','LOCAL')
    CLOUD_STORAGE_ACCESS_KEY = os.getenv('CLOUD_STORAGE_ACCESS_KEY')
    CLOUD_STORAGE_SECRET_KEY = os.getenv('CLOUD_STORAGE_SECRET_KEY')
    CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET',)
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class LogConfig(object):
    # Logging Setup
    LOG_TYPE = os.getenv("LOG_TYPE", "stream")  # Default is a Stream handler
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # File Logging Setup
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    WWW_LOG_ENABLE = os.getenv('WWW_LOG_ENABLE', True)
    APP_LOG_NAME = os.getenv("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = os.getenv("WWW_LOG_NAME", "www.log")
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 100_000_000))  # 100MB in bytes
    LOG_COPIES = int(os.getenv("LOG_COPIES", 5))
class MailConfig(object):
    # main config
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings

    MAIL_ENABLED = bool(os.getenv('MAIL_ENABLED',True))
    MAIL_SERVER =  os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT',465))

    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS',False)
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL',True)

    MAIL_USE_TLS=True
    MAIL_USE_SSL=False

    MAIL_MAX_EMAILS = int(os.getenv('MAIL_MAX_EMAILS'))

    # email authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_USERNAME = ''
    # MAIL_PASSWORD = ''

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # website admin email
    ADMIN_EMAIL = ''

class ThawaniConfig(object):
    PUBLIC_KEY = os.getenv('PUBLIC_KEY','')
    SECRET_KEY = os.getenv('SECRET_KEY','')
    BASE_URL = os.getenv('BASE_URL','')
    CURR_ADD = os.getenv('CURR_ADD','')

    CANCEL_URL = os.getenv('CANCEL_URL','')
    SUCCESS_URL = os.getenv('SUCCESS_URL','')