from copy import copy
import json

from depot.manager import DepotManager
from flask import Flask
from config import FileUploadConfig

AVATAR_DEPOT = 'avatar'
MEDIA_DEPOT = 'media'

DEPOTS = {
    AVATAR_DEPOT: {'depot.prefix': 'avatars/'},
    MEDIA_DEPOT: {'depot.prefix': 'medias/'}
}


def init_depots(app: Flask):
    """Setup all configured depots"""

    config = default_config(app)


    for (name, special_config) in DEPOTS.items():
        depot_config = copy(config)
        if FileUploadConfig.STORAGE != 'LOCAL':
            depot_config.update(special_config)
        DepotManager.configure(name, depot_config)


def default_config(app: Flask):
    """Return a default config that is used by all depots"""

    if FileUploadConfig.STORAGE == 'LOCAL':
        return local_config(app)
    elif FileUploadConfig.STORAGE == 'GCP':
        return gcp_config(app)
    elif FileUploadConfig.STORAGE == 'AWS':
        return aws_config(app)
    else:
        return test_config(app)


def test_config(app: Flask):
    """Return the default test config that is used by all depots"""
    return {'depot.backend': 'depot.io.memory.MemoryFileStorage'}

def local_config(app: Flask):
    """Return the default test config that is used by all depots"""
    return {'depot.storage_path': FileUploadConfig.UPLOAD_FOLDER}


def gcp_config(app: Flask):
    """Return the default production config that is used by all depots"""

    return {
        'depot.backend': 'depot.io.boto3.S3Storage',
        'depot.endpoint_url': 'https://storage.googleapis.com',
        'depot.access_key_id': app.config.get('CLOUD_STORAGE_ACCESS_KEY'),
        'depot.secret_access_key': app.config.get('CLOUD_STORAGE_SECRET_KEY'),
        'depot.bucket': app.config.get('CLOUD_STORAGE_BUCKET')
    }

def aws_config(app: Flask):
    """Return the default production config that is used by all depots"""

    return {
        'depot.backend': 'depot.io.boto3.S3Storage',
        'depot.endpoint_url': 'https://storage.googleapis.com',
        'depot.access_key_id': app.config.get('CLOUD_STORAGE_ACCESS_KEY'),
        'depot.secret_access_key': app.config.get('CLOUD_STORAGE_SECRET_KEY'),
        'depot.bucket': app.config.get('CLOUD_STORAGE_BUCKET')
    }


def make_middleware(app):
    """Make the depot middle to serve uploads through the /depot endpoint"""
    app.wsgi_app = DepotManager.make_middleware(app.wsgi_app, mountpoint='/'+FileUploadConfig.UPLOAD_FOLDER, cache_max_age=604800, replace_wsgi_filewrapper=True)