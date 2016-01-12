from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from app import app, db
from models import User, Branch, Note, Portal

admin = Admin(app)
admin.add_view(ModelView(User, name='Users'))
admin.add_view(ModelView(Portal, name='Payment Portals'))
admin.add_view(ModelView(Branch, name='Branches'))
admin.add_view(ModelView(Note, name='Notes'))
