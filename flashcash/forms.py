from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email

class NameEmailUsernamePasswordForm(Form):
    name = TextField('Real Name', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    
