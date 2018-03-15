import os

# /justdo
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/justdo')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'please-change-this-key')
