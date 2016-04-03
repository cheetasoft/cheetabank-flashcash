from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField, FormField, FieldList, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, NumberRange

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

class NoteUnlockForm(Form):
    note_id = TextField('Note ID')
    unlock_code = TextField('Unlock Code')

class PortalNotesForm(Form):
    portal = SelectField('Portal', validators=[Required()])
    notes = FieldList(FormField(NoteUnlockForm, 'Note'), min_entries=4, max_entries=24)

class ValueCountForm(Form):
    value = DecimalField('Value of each note',
        places=1,
        default=5.0,
        validators=[Required()])
    count = IntegerField('Number of notes',
        default=6,
        validators=[Required(), NumberRange(min=0, max=20)])
    
