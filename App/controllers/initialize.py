from .user import create_driver
from App.database import db
from .street import create_street
from .user import create_resident


def initialize():
    db.drop_all()
    db.create_all()

    streets_str = ['Randy Street', 'Author Street', 'Murray Drive', 'Charles Avenue']
    streets = [create_street(street) for street in streets_str]

    create_driver('bob', 'bobpass', 'Terrence', 'Murray')
    create_resident('rick', 'rickpass', 'Rick', 'Smith', streets[0])
