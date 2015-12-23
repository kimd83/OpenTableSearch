import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    # SSL_DISABLE=False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
   
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/findtable'

config = {
    'default': DevelopmentConfig
}

print(os.environ['DATABASE_URL'])