from flask import current_app
from config import BaseConfig, FileUploadConfig
from dateutil.parser import parse


def is_exisit_in_request(data, param):
    if param not in data or data[param] is None:
        return False
    else :
        return True

def not_exisit_in_request(data, param, default=None):
    try:
        if param not in data or data[param] is None:
            return default
        else:
            return data[param]
    except Exception as e:
        current_app.logger.error(e)
        #print(param)
        #print(e)
        return default
def get_media_url(file):
    files_url = {}
    try:
        if file == None:
            return files_url
        if '_public_url' in file and file['_public_url'] != None:
            files_url.update({'file':file['_public_url']})
        else:
            path = file['path']
            files_url.update({'file':BaseConfig.HOST_URL + '/'+ FileUploadConfig.UPLOAD_FOLDER + '/' + path + '/' + file['filename']})
        if '_thumb_public_url' in file and file['_thumb_public_url'] != None:
            files_url.update({'thumb':file['_thumb_public_url']})
        else:
            if 'thumb_path' in file and file['thumb_path'] != None:
                path = file['thumb_path']
                files_url.update({'thumb':BaseConfig.HOST_URL + '/'+ FileUploadConfig.UPLOAD_FOLDER + '/' + path + '/' + file['filename']})
        return files_url
    except Exception as e:
        current_app.logger.error(e)
        return files_url

def to_datetime(date_str):
    try:
        if date_str is None:
            return date_str
        return parse(date_str, dayfirst=True)
    except Exception as e:
        current_app.logger.error(e)
        return date_str