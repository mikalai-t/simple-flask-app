import os

basedir = os.path.abspath(os.path.dirname(__file__))


# full list of possible config options see at: http://flask.pocoo.org/docs/1.1.x/config/

class Config(object):
    ENV = 'Development'
    DEBUG = False
    CSRF_ENABLED = False
    # to avoid RuntimeError exception calling `flash`ed methods, a secret key must be set!
    SECRET_KEY = os.urandom(16)
    MAX_CONTENT_LENGTH = int(524288000)


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    ENV = 'Production'
    CSRF_ENABLED = True
