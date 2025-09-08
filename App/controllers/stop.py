from App import Driver, Street, Stop
from App.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def create_stop(driver: Driver, street: Street, scheduled_date: str) -> Stop | None:
    try:
        new_stop = Stop(driver, street, scheduled_date)

        db.session.add(new_stop)
        db.session.commit()
        return new_stop
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Failed to create stop on {street.name}")
        return None