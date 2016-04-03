from itsdangerous import URLSafeTimedSerializer
import string
import random
from ..app import app
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def random_id(size=6, chars=string.ascii_letters + string.digits):
    '''Generate a random string used for FlashCash notecodes'''
    return ''.join(random.choice(chars) for _ in range(size))
