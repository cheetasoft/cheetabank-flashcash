from flask import render_template, flash, request, url_for, redirect, abort
from app import app
from auth import login_manager, current_user, login_required
from models import User, Branch, Note
from forms import NameEmailUsernamePasswordForm
from util.security import ts
from util.email import send_email

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.htm')

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = NameEmailUsernamePasswordForm()
    if form.validate_on_submit():
        # Check for existing username
        if User.select().where(User.username == form.data['username']).exists():
            msg = 'Username already exists! Please try a different one'
            if form.errors.has_key('username'):
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
            send_email(u.email, subject, html)

            return redirect(url_for('index'))
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

    return redirect(url_for('login'))
