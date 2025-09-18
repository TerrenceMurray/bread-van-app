from App.models import StopRequest
from App.database import db
from typing import TYPE_CHECKING
from .notification import create_notification
from .. import NotificationType, get_street_by_string

if TYPE_CHECKING:
    from App.models import Resident, Street

'''
CREATE
'''
def create_stop_request(resident: Resident):
    """
    Create a stop request for a resident's street
    """
    db.session.add(StopRequest(resident))
    db.session.commit()

    create_notification(
        message=f"'{resident.get_fullname()}' has requested a stop for street '{resident.street_name}'.",
        notification_type=NotificationType.REQUESTED,
        street=get_street_by_string(resident.street_name)
    )

def stop_request_exists(street_name: str) -> bool:
    """
    Check if a stop request exists already
    """
    return db.session.query(StopRequest).filter_by(street_name=street_name).first() is not None


'''
DELETE
'''
def delete_stop_requests(street: Street) -> None:
    """
    Delete all stop requests for a street
    """
    db.session.delete(
        db.session.query(StopRequest).filter_by(street_name=street.name).all()
    )
    db.session.commit()