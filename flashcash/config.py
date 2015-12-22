import os.path

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = 'This is supposedly secret'
    DEBUG = True

    DATABASE = {
        'name': 'flashcash.sqlite',
        'engine': 'peewee.SqliteDatabase',
    }

