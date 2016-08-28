from ..app import app, mail
from flask.ext.mail import Message
def send_email(email, subject, message):
    if app.config['DEBUG']:
        print '==== Sending new email ===='
        print 'To: %s' % email
        print 'Subject: %s' % subject
        print message
        print '======= End of email ======='
    # TODO: Add actual email-sending code here!
    m = Message(subject, recipients=[email])
    m.body = message
    mail.send(m)
