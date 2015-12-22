from models import *

def create_tables():
    db.database.create_tables([User, Branch, Note])
