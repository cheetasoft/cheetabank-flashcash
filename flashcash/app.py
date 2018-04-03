from flask import Flask
from flask.ext.peewee.db import Database
from flask.ext.mail import Mail
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
try:
    app.config.from_pyfile('../instance/config.py')
except:
    app.logger.warning('Warning: Using default config!')
    app.config.from_object('flashcash.config.Config')

db = Database(app)
mail = Mail(app)

if 'LOG_FILE' in app.config:
    handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
