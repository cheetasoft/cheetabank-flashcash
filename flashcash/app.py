from flask import Flask
from flask.ext.peewee.db import Database

app = Flask(__name__)
app.config.from_object('flashcash.config.DevelopmentConfig')
app.config.from_pyfile('../instance/config.py')

db = Database(app)
