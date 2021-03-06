from flask import render_template, flash, request, url_for, redirect, abort
from .app import app
from .auth import login_manager, current_user, login_required
from .admin import admin_permission, manager_permission
from .models import db, User, Branch, Note, Portal, Transaction, TransactionNotes
from datetime import datetime
from . import forms
from .util.security import ts
from .util.email import send_email

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/about/')
def about():
    return render_template('about.htm')

@app.route('/dashboard/')
@login_required
def dashboard():
    # Allow admins and managers to access admin page
    allow_admin = admin_permission.can() or manager_permission.can()
    return render_template('dashboard.htm', allow_admin=allow_admin)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = forms.NameEmailUsernamePasswordForm()
    if form.validate_on_submit():
        # Check for existing username
        if User.select().where(User.username == form.data['username']).exists():
            msg = 'Username already exists! Please try a different one'
            if 'username' in form.errors:
                form.errors['username'].append(msg)
            else:
                form.errors['username'] = [msg]
        else:
            u = User()
            u.name = form.data['name']
            u.email = form.data['email']
            u.username = form.data['username']
            u.password = form.data['password']
            u.save(force_insert=True)

            # Send email
            subject = 'Confirm your FlashCash account'
            token = ts.dumps(u.email, salt='email-confirm-key')
            confirm_url = url_for('confirm_email',
                token = token,
                _external=True)
            html = render_template('email/activate.htm', name=u.name, confirm_url=confirm_url)
            text = render_template('email/activate.txt', name=u.name, confirm_url=confirm_url)
            send_email(u.email, subject, text, html)

            return redirect(url_for('dashboard'))
    return render_template('accounts/signup.htm', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        u = User.get(email=email)
    except:
        abort(404)

    u.email_confirmed = True
    u.save()
    flash('Your email address has been confirmed!')

    return redirect(url_for('dashboard'))

@app.route('/dashboard/portals/')
@login_required
def dash_portals():
    return render_template('portals/index.htm')

@app.route('/dashboard/portals/add', methods=['GET', 'POST'])
@login_required
def add_portal():
    form = forms.PortalShopForm()
    if form.validate_on_submit():
        if Portal.select().where(Portal.portal_code == form.data['portal_code']).exists():
            msg = 'Somebody has already tried to register that portal-code'
            if 'portal_code' in form.errors:
                form.errors['portal_code'].append(msg)
            else:
                form.errors['portal_code'] = [msg]
        else:
            p = Portal(portal_code=form.data['portal_code'],
                shop_name=form.data['shop_name'],
                owner=current_user.username)
            p.save()
            flash('Please ask your Branch Manager to confirm your portal code before you begin using it.')
            return redirect(url_for('dash_portals'))
    return render_template('portals/add.htm', form=form)

@app.route('/dashboard/notes/add/', methods=['GET', 'POST'])
@login_required
def claim_notes():
    form = forms.PortalNotesForm()
    portal_choices = [(p.portal_code, '%s (%s)' % (p.shop_name, p.portal_code)) for p in current_user.portals]
    form.portal.choices = portal_choices
    if form.validate_on_submit():
        notes_to_add = []
        total_sum = 0
        errors = False
        try:
            portal = Portal.get(portal_code=form.portal.data, owner=current_user.username, confirmed=True)
        except Portal.DoesNotExist:
            if not form.portal.errors: form.portal.errors = []
            form.portal.errors.append('You are not authorized to use that Portal')
            errors = True

        for note in form.notes:
            if not (note.note_id.data or note.unlock_code.data): continue
            try:
                n = Note.get(note_id=note.note_id.data, unlock_code=note.unlock_code.data)
                if n.claimer is not None:
                    if not note.name in form.errors: form.errors[note.name] = []
                    form.errors[note.name].append('This note has already been claimed')
                    errors = True
                    continue
                # All fine; add notes to list
                notes_to_add.append(n)
                total_sum += n.value
            except Note.DoesNotExist:
                if not note.name in form.errors: form.errors[note.name] = []
                form.errors[note.name].append('Invalid Note ID or Unlock Code')
                errors = True
                continue
        if not errors:
            with db.database.atomic():
                # Create transaction
                t = Transaction()
                t.date = datetime.now()
                t.portal = portal
                t.amount = total_sum
                t.save()
                for n in notes_to_add:
                    n.claimer = current_user.username
                    n.save()
                    TransactionNotes.create(transaction=t, note=n)
            flash('%d SSS has been successfully added to your account' % t.amount)
            return redirect(url_for('dashboard'))
    return render_template('notes/add.htm', form=form)

@app.route('/dashboard/profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = forms.NameEmailForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        if current_user.email != form.email.data:
            old_email = current_user.email
            current_user.email = form.email.data
            current_user.email_confirmed = False
            email_changed = True
        else:
            email_changed = False
        current_user.save()
        flash('Your changes have been saved.')
        if email_changed:
            # Send email
            subject = 'Confirm your new email address'
            token = ts.dumps(current_user.email, salt='email-confirm-key')
            confirm_url = url_for('confirm_email',
                token = token,
                _external=True)
            text = render_template('email/confirm_email.txt', name=current_user.name, confirm_url=confirm_url)
            html = render_template('email/confirm_email.htm', name=current_user.name, confirm_url=confirm_url)
            send_email(current_user.email, subject, text, html)
            flash('Please check your inbox to confirm your new email address.')

            # Send notification to old email
            subject = 'Alert: Email address changed'
            text = render_template('email/email_change_alert.txt',
                name=current_user.name,
                new_email=current_user.email)
            html = render_template('email/email_change_alert.htm',
                name=current_user.name,
                new_email=current_user.email)
            send_email(old_email, subject, text, html)

    return render_template('accounts/edit.htm', form=form)
