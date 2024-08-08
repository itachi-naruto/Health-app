#from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import BaseConfig

engine = BaseConfig().engine
Base = declarative_base()

def init_model():
    import app.users.model
    import app.patients.model
    import app.doctors.model
    import app.medias.model
    import app.centers.model
    import app.payment_transaction.model
    import app.setting.model
    import app.specialties.model
    import app.status.model
    import app.appointments.model
    import app.cases.model
    import app.schedules.model
    import app.chat.model
    import app.reviews.model
    import app.Complains.model
    import app.favorite.model
    import app.invoice.model
    import app.earning.model

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    init_model()
    Base.metadata.create_all(bind=engine, checkfirst=True)