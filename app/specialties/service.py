## service layer of the API
import json
import os,base64
import uuid
import sqlalchemy as sql
from flask import current_app, url_for
from sqlalchemy.orm.query import Query
from config import BaseConfig
from .model import Specialty
from werkzeug.utils import secure_filename
from config import FileUploadConfig

        # Allowed extensions for file upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER =  os.path.abspath('app/uploads/')

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class SpecialtyService:
    def __init__(self):
        self.eng = BaseConfig().engine

        # Create a session
        self.Session = sql.orm.sessionmaker()
        self.Session.configure(bind=self.eng)
        self.session = self.Session()
       

        
        # Create uploads directory if it doesn't exist
        if not os.path.exists('app/uploads'):
            os.makedirs('app/uploads')


    def getSpecialties(self, id): 
        try:
            if id is None:
                specialties = self.session.query(Specialty).all()
            else:
                specialties = self.session.query(Specialty).filter(Specialty.id==id).all()
            
            result = []

            for specialty in specialties:
                data = {}
                data['id'] = specialty.id
                data['name'] = specialty.name
                data['name_ar'] = specialty.name_ar
                data['image'] = specialty.image


                result.append(data)

            return result
        except Exception as e:
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    
    def createspecialty(self,files, data):
        try:
            for file in files:
                if not allowed_file(file.filename):
                    return {'message': 'File type not allowed', 'status': 400}

                # Validate file content if necessary [application/pdf', 'text/plain']
                if file.mimetype not in ['image/jpeg', 'image/png']:
                    return {'message': 'Invalid file type', 'status': 400}

                # Save the file to the server
                filename = secure_filename(file.filename)
                       # Generate a unique filename using uuid
                extension = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{extension}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file_url = url_for('specialties.uploaded_file', filename=unique_filename, _external=True)
                try:
                    file.save(file_path)
                except IOError as e:
                    return {'message': f'Could not save file: {str(e)}', 'status': 500}
                
                if not data or not 'name' in data or not 'name_ar' in data:
                    return 'data is required.', 422
                name = data['name']
                name_ar = data['name_ar']
                if not name:
                    return 'Name is required.', 422
                if not name_ar:
                    return 'Arabic name is required.', 422
                    # Save file reference to the database
                specialty = Specialty(name=name,image=file_url,name_ar=name_ar,)

                self.session.add(specialty)
                self.session.commit()

            #return 'Created', 201
                return {'message': 'Files uploaded successfully', 'status': 201}
     

        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()
            
    def updateSpecialty(self, id, data):
        try:
            specialty = self.session.query(Specialty).filter(Specialty.id==id).first()

            specialty.name = data['name']
            specialty.image = data['image']

            self.session.commit()

            return 'Updated', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()

    def deleteSpecialty(self, id):
        try:
            specialty = self.session.query(Specialty).filter(Specialty.id==id).first()

            if specialty == None:
                return 'Not Found', 404
            
            self.session.delete(specialty)
            self.session.commit()

            return 'Deleted', 200
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            return "{}".format('Internal Server Error'), 500
        finally:
            self.session.close()


    def uploadBase64(data):
               # Validate presence of filename and filedata
            if 'picname' not in data or 'image' not in data:
                return {'error': 'Filename and filedata are required'}, 400

            filename = data['picname']
            pic = data['image']

            # Validate the filename extension
            if not allowed_file(filename):
                return {'error': 'File type not allowed'}, 400
            
            try:
                # Decode the base64 filedata
                file_content = base64.b64decode(pic)
            except base64.binascii.Error:
                return {'error': 'Invalid base64 encoding'}, 400

            # Define the full file path
            file_path = os.path.join(FileUploadConfig.UPLOAD_FOLDER, filename)

            try:
                # Write the decoded content to a file
                with open(file_path, 'wb') as f:
                    f.write(file_content)
            except IOError as e:
                return {'error': f'Could not save file: {str(e)}'}, 500         