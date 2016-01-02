from flask_login import UserMixin
from app import db
import peewee as pw

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('?', 'Unknown')
    )

class User(db.Model, UserMixin):
    name = pw.CharField()
    username = pw.CharField(max_length=32, primary_key=True)
    password = pw.CharField(max_length=128)
    email = pw.CharField(null=True)
    email_confirmed = pw.BooleanField(default=False)

class Portal(db.Model):
    portal_code = pw.CharField(max_length=2)
    shop_name = pw.CharField(max_length=32)
    owner = pw.ForeignKeyField(User)
    balance = pw.DecimalField(decimal_places=2, default=0)

class Branch(db.Model):
    id = pw.CharField(max_length=6, primary_key=True)
    name = pw.CharField(max_length=32)

class Note(db.Model):
    note_id = pw.CharField(max_length=6)
    passcode = pw.CharField(max_length=6)
    branch = pw.ForeignKeyField(Branch)
    value = pw.DecimalField(decimal_places=2, default=0)
    claimer = pw.ForeignKeyField(User, null=True)
