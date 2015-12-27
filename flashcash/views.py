from flask import render_template, flash, request, url_for, redirect, abort
from app import app
from auth import login_manager, current_user, login_required
from models import User, Branch, Note
import wtforms as wtf

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.htm')
