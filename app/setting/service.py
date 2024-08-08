## service layer of the API
import json
import sqlalchemy as sql
from flask import current_app
from sqlalchemy.orm.query import Query
from config import BaseConfig
from .model import Setting
from datetime import datetime

class SettingService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getSettingModel(self, settings):
        result = []
        for setting in settings:
            data = {}
            data['category'] = setting.category
            data['key'] = setting.key
            data['value'] = setting.value
            data['last_modified'] = setting.last_modified
            result.append(data)
        return result

    def getSettings(self, key): 
        try:
            if key is None:
                settings = self.session.query(Setting).all()
            else:
                settings = self.session.query(Setting).filter(key=key).all()

            return self.getSettingModel(settings)
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()
    
    def getSettingsByCategory(self, category): 
        try:
            settings = self.session.query(Setting).filter(category=category).all()

            return self.getSettingModel(settings)
        except Exception as e:
            return "{}".format(e), 500
        finally:
            self.session.close()

    def updateSetting(self, key, data):
        try:
            setting = self.session.query(Setting).filter(key==key).first()

            setting.category = data['category']
            setting.value = data['value']
            setting.last_modified = datetime.datetime.now()

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()
    
    def createSetting(self, data):
        try:
            setting = Setting(
                key=data['key'],
                category=data['category'],
                value=data['value'],
                last_modified = datetime.datetime.now()
            )
            self.session.add(setting)
            self.session.commit()

            return 'Setting Created', 201, True
        except Exception as e:
            #current_app.logger.error(e)
            self.session.rollback()
            return "{}".format(e), 500, False
        finally:
            self.session.close()
    
    def deleteSetting(self, key):
        try:
            setting = self.session.query(Setting).filter_by(key=key).first()

            if setting == None:
                return 'Not Found', 404
            
            self.session.delete(setting)
            self.session.commit()

            return 'Setting deleted', 200
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()
            