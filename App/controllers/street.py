from App.models import Street
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def get_street_by_string(street_str: str) -> Street | None:
    return db.session.query(Street).filter_by(name=street_str).one_or_none()

def get_all_streets() -> list[Street]:
    return db.session.scalars(db.select(Street)).all()

def get_all_streets_json() -> list[dict[str, str]]:
    streets = get_all_streets()
    if not streets:
        return []
    return [street.get_json() for street in streets]

def create_street(street: str) -> Street | None:
    try:
        new_street = Street(name=street)
        db.session.add(new_street)
        db.session.commit()
        return new_street
    except SQLAlchemyError as e:
        db.session.rollback()
        # log or re-raise depending on context
        print(f"Failed to create street '{street}': {e}")
        return None