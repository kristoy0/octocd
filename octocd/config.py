class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/octocd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'DEV_KEY'
