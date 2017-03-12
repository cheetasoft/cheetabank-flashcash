from flask import Flask
from flask.ext.peewee.db import Database
from flask.ext.mail import Mail

app = Flask(__name__)
try:
    app.config.from_pyfile('../instance/config.py')
except:
    app.logger.warning('Warning: Using default config!')
    app.config.from_object('flashcash.config.Config')

db = Database(app)
mail = Mail(app)
