from flask.ext.admin import Admin, BaseView, expose
from flask_admin.contrib.peewee import ModelView

from .app import app, db
from .auth import Permission, RoleNeed, current_user
from flask import flash, redirect, url_for
from .models import User, Branch, Note, Portal, pw
from .forms import ValueCountForm
from .util.security import random_id

manager_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

class ManagerModelView(ModelView):
    def is_accessible(self):
        return manager_permission.can() or admin_permission.can()

class AdminModelView(ModelView):
    def is_accessible(self):
        return admin_permission.can()

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(AdminModelView(User, name='Users'))
admin.add_view(AdminModelView(Portal, name='Payment Portals'))
admin.add_view(AdminModelView(Branch, name='Branches'))
admin.add_view(ManagerModelView(Note, name='Notes'))

class GenerateNotesView(BaseView):
    def is_accessible(self):
        # Managers only: non-manager admins not allowed
        return manager_permission.can()

    @expose('/', methods=['GET', 'POST'])
    def generate(self):
        form = ValueCountForm()
        if form.validate_on_submit():
            # Generate notes
            value = form.value.data
            added_notes = []
            for _ in range(form.count.data):
                while True:
                    try:
                        n = Note.create(note_id=random_id(),
                            unlock_code=random_id(),
                            branch=current_user.manager_of,
                            value=value)
                        added_notes.append(n)
                        break
                    except pw.IntegrityError:
                        # Note with ID already exists
                        continue
            msg = '%d notes of value %.2f added successfully' % (
                len(added_notes),
                value)
            flash(msg)
            return redirect(url_for('admin.index'))

        return self.render('admin/generate_notes.htm', form=form)

admin.add_view(GenerateNotesView(name='Generate notes'))
