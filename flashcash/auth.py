from .app import app, db
from .models import User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import wtforms as wtf
from flask_wtf import Form
from flask import render_template, redirect, url_for, request, flash, current_app, session
from flask.ext.principal import Principal, Permission, RoleNeed, UserNeed, Identity, AnonymousIdentity, identity_changed, identity_loaded
from .forms import UsernamePasswordForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

principals = Principal(app)

@login_manager.user_loader
def load_user(username):
    try:
        user = User.get(username=username)
    except User.DoesNotExist:
        return None
    return user

# Setup principals

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Add roles
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = load_user(form.username.data)
        if (not user) or (user.check_password and not user.check_password(form.password.data)):
            msg = 'Invalid username or password'
            if form.errors.has_key('password'):
                form.errors['password'].append(msg)
            else:
                form.errors['password'] = [msg]
        else:
                    # All OK. Log in the user.
                login_user(user)
                # Inform Principal of changed identity
                identity_changed.send(
                    current_app._get_current_object(),
                    identity=Identity(str(user.id)))
        
                return redirect(request.args.get('next') or url_for('dashboard'))
        # Default to returning login page        
    return render_template('login.htm', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('You are now logged out.')

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())
    
    return redirect(request.args.get('next') or url_for('login'))
