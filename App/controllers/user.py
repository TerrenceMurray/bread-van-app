from App.models import User, Driver
from App.database import db

def create_user(username, password, first_name, last_name) -> User:
    newuser = User(username=username, password=password, first_name=first_name, last_name=last_name)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_driver(username, password, first_name, last_name) -> Driver:
    new_driver = Driver(
        username,
        password,
        first_name,
        last_name
    )

    db.session.add(new_driver)
    db.session.commit()
    return new_driver

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_drivers():
    return db.session.scalars(db.select(Driver)).all()

def get_all_drivers_json():
    drivers = get_all_drivers()
    if not drivers:
        return []
    drivers = [driver.get_json() for driver in drivers]
    return drivers

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

