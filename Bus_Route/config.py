import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True    
    SECRET_KEY = 'thisisasecret'
    IMAGE_UPLOADS = r"C:\Users\Mini Aishwarya\Documents\Project\Web-app\Bus_Route\app\static\images\uploads"
    ALLOWED_IMAGE_EXTENSIONS = ["PNG", "JPG", "JPEG"]

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
