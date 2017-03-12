from ..app import app, mail
from flask.ext.mail import Message
def send_email(email, subject, text, html):
    if app.config['DEBUG']:
        app.logger.debug('==== Sending new email ====')
        app.logger.debug('To: %s' % email)
        app.logger.debug('Subject: %s' % subject)
        app.logger.debug('\n======= Text version =======\n')
        app.logger.debug(text)
        app.logger.debug('\n======= HTML version =======\n')
        app.logger.debug(html)
        app.logger.debug('======= End of email =======')
    # TODO: Add actual email-sending code here!
    m = Message(subject, recipients=[email])
    m.message = text
    m.html = html
    mail.send(m)
