from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, Length

class NameEmailUsernamePasswordForm(Form):
    name = TextField('Real Name', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class PortalShopForm(Form):
    portal_code = TextField('Portal Code', validators=[
        Required(),
        Length(min=2, max=2,
            message='Please enter a valid Cheetplaza Portal Code'),
        ])
    shop_name = TextField('Shop Name', validators=[Required()])

class UsernamePasswordForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    
