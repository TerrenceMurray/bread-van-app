from .user import create_driver
from App.database import db
from .street import create_street


def initialize():
    db.drop_all()
    db.create_all()
    create_driver('bob', 'bobpass', 'Terrence', 'Murray')

    streets = ['Randy Street', 'Author Street', 'Murray Drive', 'Charles Avenue']
    for street in streets:
        create_street(street)
