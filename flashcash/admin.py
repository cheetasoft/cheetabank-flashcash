from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from .app import app, db
from .auth import Permission, RoleNeed
from .models import User, Branch, Note, Portal

manager_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

class ManagerModelView(ModelView):
    def is_accessible(self):
        return manager_permission.can() or admin_permission.can()

class AdminModelView(ModelView):
    def is_accessible(self):
        return admin_permission.can()

admin = Admin(app)
admin.add_view(AdminModelView(User, name='Users'))
admin.add_view(AdminModelView(Portal, name='Payment Portals'))
admin.add_view(AdminModelView(Branch, name='Branches'))
admin.add_view(ManagerModelView(Note, name='Notes'))
