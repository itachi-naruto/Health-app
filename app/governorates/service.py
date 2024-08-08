import sqlalchemy as sql

from flask import current_app
from sqlalchemy.orm import joinedload

from .model import Governorate, Wilayat
from config import BaseConfig


class LocationService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()

    def getGovernorates(self):
        try:
            governorates = self.session.query(Governorate).all()
            result = []  

            for governorate in governorates:
                governorate_data = {}   
                governorate_data['id'] = governorate.id
                governorate_data['Governorate Name'] = governorate.g_name
                governorate_data['Main Wilayat'] = governorate.main_wilayat
                governorate_data['Total Wilayat'] = governorate.total_wilayat
                
                result.append(governorate_data)

            return result
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def getWilayats(self):
        try:

            wilayats = self.session.query(Wilayat).all()
            result = []  

            for wilayat in wilayats:
                wilayat_data = {}   
                wilayat_data['id'] = wilayat.id
                wilayat_data['Wilayat Name'] = wilayat.w_name
                
                result.append(wilayat_data)

            return result
        except Exception as e:
            self.session.rollback()
            return "{}".format(e), 500
        finally:
            self.session.close()

    def addGovernorate(self, data):
        try:
            check_governorate = self.session.query(Governorate).filter(Governorate.g_name == data['g_name']).first()

            if check_governorate:
                return "Governorate already exist", 400
            
            governorate = Governorate(
            g_name=data['g_name'], 
            main_wilayat=data['main_wilayat'],
            total_wilayat=data['total_wilayat'])

            self.session.add(governorate)
            self.session.commit()

            return 'Added Governorate details', 201
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def addWilayat(self, data):
        try:
            check_wilayat = self.session.query(Wilayat).filter(Wilayat.w_name == data['w_name']).first()

            if check_wilayat:
                return "Wilayat already exist", 400

            wilayat = Wilayat(
            w_name=data['w_name'], 
            g_id=data['g_id'])

            self.session.add(wilayat)
            self.session.commit()

            return 'Added Wilayat details', 201
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()   

    # def getGovernorateById(self, id):
    #     try:
    #         governorate_row = self.session.query(Governorate, Wilayat).join(Governorate.wilayats).options(joinedload(Governorate.wilayats)).filter(Governorate.id == id).first()

    #         if not governorate_row:
    #             return "Governorate not found", 404

    #         governorate = governorate_row.Governorate

    #         governorate_dict = {
    #             "id": governorate.id,
    #             "g_name": governorate.g_name,
    #             "main_wilayat": governorate.main_wilayat,
    #             "total_wilayat": governorate.total_wilayat,
    #             "wilayats":governorate_row.Wilayat.w_name,
    #         }

    #         return governorate_dict, 200

    #     except Exception as e:
    #         return  str(e), 500

    #     finally:
    #         self.session.close()

    def getGovernorateById(self, id):
        try:
            governorate = self.session.query(Governorate).options(joinedload(Governorate.wilayats)).filter(Governorate.id == id).first()

            if not governorate:
                return "Governorate not found", 404

            governorate_dict = {
                "Governorate id": governorate.id,
                "Governorate name": governorate.g_name,
                "Main Wilayat": governorate.main_wilayat,
                "Total Wilayats": governorate.total_wilayat,
                "Wilayats in the Governorate": [{"id": wilayat.id, "name": wilayat.w_name} for wilayat in governorate.wilayats],
            }

            return governorate_dict, 200

        except Exception as e:
            return str(e), 500

        finally:
            self.session.close() 

    def getWilayatById(self, id):
        try:
            wilayat = self.session.query(Wilayat).options(joinedload(Wilayat.governorates)).filter(Wilayat.id == id).first()

            if not wilayat:
                return "Wilayat not found", 404

            wilayat_dict = {
                "Wilayat id": wilayat.id,
                "Wilayat name": wilayat.w_name,
                "Governorate":  wilayat.governorates.g_name
            }

            return wilayat_dict, 200

        except Exception as e:
            return str(e), 500

        finally:
            self.session.close()
