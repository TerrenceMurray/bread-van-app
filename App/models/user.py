from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .enums import DriverStatus
from .street import Street
from abc import abstractmethod


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def set_password(self, password) -> None:
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_fullname(self) -> str:
        """Get user's fullname."""
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def view_inbox(self) -> None:
        pass

class Driver(User):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    status = db.Column(db.String(), nullable=False, default=DriverStatus.INACTIVE.value)
    current_location = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'driver'
    }

    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name)
        self.status = DriverStatus.INACTIVE.value

    def get_json(self) -> dict[str, any]:
        return {
            **super().get_json(), # dict unpack
            'status': self.status,
            'current_location': self.current_location
        }

    def get_current_status(self) -> str:
        """Get the current status and location of the driver"""
        return f'{self.get_fullname()} is currently {self.status} at {self.current_location}'

    def schedule_stop(self, street: Street, date: str) -> bool:
        """Schedule a stop for a given street"""
        return False

    def mark_arrival(self, street) -> bool:
        """Update stop to complete"""
        return False

    def update_status(self, driver_status: DriverStatus) -> None:
        """Update the driver status"""
        return

    def view_inbox(self) -> None:
        """View stop request notifications"""
        return

    def __repr__(self):
        return f"<Driver {self.id} {self.get_current_status()}>"

class Resident(User):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    street_name = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'resident'
    }

    def __init__(self, username, password, first_name, last_name, street_name):
        super().__init__(username, password, first_name, last_name)
        self.street_name = street_name

    def get_json(self) -> dict[str, any]:
        return {
            **super().get_json(), # dict unpack
            'street_name': self.street_name
        }

    def request_stop(self) -> bool:
        """Request a stop for this resident's street"""
        return False

    def view_inbox(self) -> None:
        """View drive stop arrival notifications"""
        return
