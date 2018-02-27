import os

# /justdo
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # use postgres database
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/justdo'
    SECRET_KEY = 'very-secret-key'
