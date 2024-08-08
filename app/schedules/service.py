## service layer of the API
import json
import sqlalchemy as sql
from flask import current_app
from sqlalchemy.orm.query import Query
from datetime import datetime
from config import BaseConfig
from .model import Schedule

class SeheduelService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getSeheduels(self, id):
        try:
            if id is None:
                schedules = self.session.query(Schedule).filter(Schedule.date_time >= datetime.today()).all()
            else:
                schedules = self.session.query(Schedule).filter(Schedule.date_time >= datetime.today()).filter(Schedule.doctor_id==id).filter(Schedule.active==1).all()
            
            result = []

            for schedule in schedules:
                data = {}
                data['id'] = schedule.id
                data['date_time'] = schedule.date_time
                data['period'] = schedule.period
                data['active'] = schedule.active
                data['doctor_id'] = schedule.doctor_id
                data['center_id'] = schedule.center_id

                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def getNextScheduel(self, id):
        try:
            schedule = self.session.query(Schedule).filter(Schedule.date_time >= datetime.today()).filter(Schedule.active==1).filter(Schedule.doctor_id==id).order_by(Schedule.date_time.asc()).first()
            
            return schedule.date_time if schedule is not None else ''
        except Exception as e:
            current_app.logger.error(e)
        finally:
            self.session.close()

    def createSeheduel(self, data):
        doctor = data['doctor_id']
        center = data['center_id']
        if not doctor:
            return 'A doctor is required.', 422
        if not center:
            return 'A center is required.', 422
        try:
            schedule = Schedule(date_time=data['date_time'],
            period=data['period'],
            doctor_id=data['doctor_id'],
            center_id=data['center_id'])

            self.session.add(schedule)
            self.session.commit()

            return 'Created', 201
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def updateSchedule(self, id, data):
        try:
            schedule = self.session.query(Schedule).filter(Schedule.id==id).first()

            schedule.date_time = data['date_time']
            schedule.period = data['period']
            schedule.center_id = data['center_id']
            schedule.active = data['active']

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def bookSchedule(self, id):
        try:
            schedule = self.session.query(Schedule).filter(Schedule.id==id).first()

            schedule.active = 0

            self.session.commit()

            return 'booked', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def cancelSchedule(self, id):
        try:
            schedule = self.session.query(Schedule).filter(Schedule.id==id).first()

            schedule.active = 1

            self.session.commit()

            return 'canceled', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def deleteSchedule(self, id):
        try:
            schedule = self.session.query(Schedule).filter(Schedule.id==id).first()

            if schedule == None:
                return 'Not Found', 404
            
            self.session.delete(schedule)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()