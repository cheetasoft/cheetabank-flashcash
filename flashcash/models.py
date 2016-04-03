from flask_login import UserMixin
from .app import db
import peewee as pw

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('?', 'Unknown')
    )

class Branch(db.Model):
    branch_id = pw.CharField(max_length=6)
    name = pw.CharField(max_length=32)
    def __unicode__(self):
        return '%(id)s - %(name)s' % {
            'id': self.branch_id,
            'name': self.name
        }

class User(db.Model, UserMixin):
    name = pw.CharField()
    username = pw.CharField(max_length=32, primary_key=True)
    password = pw.CharField(max_length=128)
    email = pw.CharField(null=True)
    email_confirmed = pw.BooleanField(default=False)
    is_admin = pw.BooleanField(default=False)
    manager_of = pw.ForeignKeyField(Branch, null=True)

    @property
    def roles(self):
        roles = []
        if self.is_admin: roles.append('admin')
        if self.manager_of is not None: roles.append('manager')
        return roles
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

class Transaction(db.Model):
    date = pw.DateTimeField()
    portal = pw.ForeignKeyField(Portal)
    amount = pw.DecimalField(decimal_places=2, default=0)
    balance = pw.DecimalField(decimal_places=2, default=0) # Balance after transaction
    @property
    def notes(self):
        return TransactionNote.select().where(TransactionNote.transaction == self)

    def __unicode__(self):
        return 'Transaction on %(date)s by %(portal)s' % {
            'date': self.date,
            'portal': self.portal.portal_code
            }

class TransactionNotes(db.Model):
    note = pw.ForeignKeyField(Note)
    transaction = pw.ForeignKeyField(Transaction)
