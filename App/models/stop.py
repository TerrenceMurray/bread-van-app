from App.database import db
from .street import Street
from typing import TYPE_CHECKING
import datetime as dt

if TYPE_CHECKING:
    from .user import Driver


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(255), nullable=False)
    scheduled_date = db.Column(db.String(27), nullable=False)
    created_at = db.Column(db.String(27), nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    driver = db.relationship('Driver', back_populates='stops', lazy='joined')

    def __init__(self, driver: 'Driver', street: Street, scheduled_date: str):
        self.driver_id = driver.id
        self.street_name = street.name
        self.scheduled_date = scheduled_date

        # Defaults
        self.is_complete = False
        self.created_at = dt.datetime.utcnow().isoformat()

    def get_json(self) -> dict[str, any]:
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'street_name': self.street_name,
            'scheduled_date': self.scheduled_date,
            'created_at': self.created_at,
            'is_complete': self.is_complete
        }

    def complete(self) -> bool:
        """Mark the stop as completed"""
        return False
