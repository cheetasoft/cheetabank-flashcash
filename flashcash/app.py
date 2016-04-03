from flask import Flask
from flask.ext.peewee.db import Database

app = Flask(__name__)
try:
    app.config.from_pyfile('../instance/config.py')
except:
    print 'Warning: Using default config!'
    app.config.from_object('flashcash.config.Config')

db = Database(app)
