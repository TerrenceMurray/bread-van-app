from .user import create_driver
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_driver('bob', 'bobpass', 'Terrence', 'Murray')
