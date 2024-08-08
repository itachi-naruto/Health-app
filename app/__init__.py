import logging
from flask import Flask, request
from datetime import datetime
from database import init_db
from extensions import logs,mail
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')
    app.config.from_object('config.LogConfig')
    app.config.from_object('config.MailConfig')
    app.config.from_object('config.SMSConfig')
    app.debug = 0

    init_db()
    register_extensions(app)

    with app.app_context():
        register_blueprints(app)
    setup_depots(app)


    # swagger
    if os.environ.get('SWAGGER__ENABLED', True):
        setup_swagger(app)
    
    
    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

    return app

def register_blueprints(self):
    """Register all blueprints"""
    from .users.routes import users
    from .doctors.routes import doctors
    from .patients.routes import patients
    from .medias.routes import medias
    from .security.login import login, signup
    from .centers.routes import centers
    from .utilities.email import mails
    from .utilities.dashboard import dashboard
    from .payment_transaction.routes import payments
    from .specialties.routes import specialties
    from .setting.routes import settings
    from .appointments.routes import appointments
    from .cases.routes import cases
    from .schedules.routes import schedules
    from .chat.routes import chats
    from .reviews.routes import reviews
    from .Complains.routes import complains
    from .thawani.routes import thawani
    from .favorite.routes import favorites
    from .invoice.routes import invoices
    from .earning.routes import earnings
    from .oman_governorates.routes import governorates

    self.register_blueprint(users, url_prefix="/project/api/v1/users")
    self.register_blueprint(doctors, url_prefix="/project/api/v1/doctors")
    self.register_blueprint(patients, url_prefix="/project/api/v1/patients")
    self.register_blueprint(medias, url_prefix="/project/api/v1/medias")
    self.register_blueprint(centers, url_prefix="/project/api/v1/centers")
    self.register_blueprint(payments, url_prefix="/project/api/v1/payments")
    self.register_blueprint(settings, url_prefix="/project/api/v1/settings")
    self.register_blueprint(login, url_prefix="/project/api/v1/login")
    self.register_blueprint(signup, url_prefix="/project/api/v1/signup")
    self.register_blueprint(mails, url_prefix="/project/api/v1/email")
    self.register_blueprint(specialties, url_prefix="/project/api/v1/specialties")
    self.register_blueprint(appointments, url_prefix="/project/api/v1/appointments")
    self.register_blueprint(cases, url_prefix="/project/api/v1/cases")
    self.register_blueprint(schedules, url_prefix="/project/api/v1/schedules")
    self.register_blueprint(chats, url_prefix="/project/api/v1/chats")
    self.register_blueprint(reviews, url_prefix="/project/api/v1/reviews")
    self.register_blueprint(complains, url_prefix="/project/api/v1/complains")
    self.register_blueprint(thawani, url_prefix="/project/api/v1/thawani")
    self.register_blueprint(favorites, url_prefix="/project/api/v1/favorites")
    self.register_blueprint(invoices, url_prefix="/project/api/v1/invoices")
    self.register_blueprint(earnings, url_prefix="/project/api/v1/earnings")
    self.register_blueprint(dashboard, url_prefix="/project/api/v1/dashboard")
    self.register_blueprint(governorates, url_prefix="/project/api/v1/governorates")

def register_extensions(self):
    logs.init_app(self) #logs
    mail.init_app(self)# Initialize Flask-Mail

def setup_depots(self):
    """Setup the file depots"""
    from .config import depot
    depot.init_depots(self)
    depot.make_middleware(self)

def setup_swagger(self):
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Syhaty application"
        },
    )
    #self.register_blueprint(swagger, url_prefix="/project/swagger")
    self.register_blueprint(swaggerui_blueprint)