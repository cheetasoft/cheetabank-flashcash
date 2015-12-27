from flask import Flask
from flask.ext.peewee.db import Database

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = Database(app)
