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
    def __unicode__(self):
        return '%(username)s - %(name)s' % {
            'name': self.name,
            'username': self.username
        }

class Portal(db.Model):
    portal_code = pw.CharField(max_length=2)
    shop_name = pw.CharField(max_length=32)
    owner = pw.ForeignKeyField(User, related_name='portals')
    balance = pw.DecimalField(decimal_places=2, default=0)
    confirmed = pw.BooleanField(default=False)

    def __unicode__(self):
        return '%(portal_code)s - %(shop_name)s' % {
            'portal_code': self.portal_code,
            'shop_name': self.shop_name
        }

class Branch(db.Model):
    branch_id = pw.CharField(max_length=6)
    name = pw.CharField(max_length=32)
    def __unicode__(self):
        return '%(id)s - %(name)s' % {
            'id': self.branch_id,
            'name': self.name
        }

class Note(db.Model):
    note_id = pw.CharField(max_length=6)
    unlock_code = pw.CharField(max_length=6)
    branch = pw.ForeignKeyField(Branch)
    value = pw.DecimalField(decimal_places=2, default=0)
    claimer = pw.ForeignKeyField(User, null=True)
    def __unicode__(self):
        return '%(note_id)s - %(value)d SSS' % {
            'note_id': self.note_id,
            'value': self.value
        }
