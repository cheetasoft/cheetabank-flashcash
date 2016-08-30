from ..app import app, mail
from flask.ext.mail import Message
def send_email(email, subject, text, html):
    if app.config['DEBUG']:
        print '==== Sending new email ===='
        print 'To: %s' % email
        print 'Subject: %s' % subject
        print '\n======= Text version =======\n'
        print text
        print '\n======= HTML version =======\n'
        print html
        print '======= End of email ======='
    # TODO: Add actual email-sending code here!
    m = Message(subject, recipients=[email])
    m.message = text
    m.html = html
    mail.send(m)
