from .user import Resident
from App.database import db

class StopRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer)
    street_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(27), nullable=False)

    def __init__(self, resident: Resident):
        self.resident_id = resident.id
        self.street_name = resident.street_name
