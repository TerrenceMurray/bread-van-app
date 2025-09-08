from typing import List
from App.database import db
from App.models.notification import Notification
from App.models.street import Street
from App.models.enums import NotificationType

def create_notification(
    message: str,
    street: Street,
    notification_type: NotificationType,
) -> Notification:
    """
    Persist and return a Notification object.
    """
    notif = Notification(
        message=message,
        street=street,
        notification_type=notification_type,
    )
    db.session.add(notif)
    db.session.commit()
    return notif


def get_notifications_by_street(street: Street) -> List[Notification]:
    """
    Return all notifications for a given Street (newest first).
    """
    stmt = (
        db.select(Notification)
        .where(Notification.street_name == street.name)
        .order_by(Notification.created_at.desc())
    )
    return list(db.session.scalars(stmt).all())


def get_notifications_by_type(
    street: Street,
    notification_type: NotificationType,
) -> List[Notification]:
    """
    Return notifications for a given Street and NotificationType (newest first).
    """
    stmt = (
        db.select(Notification)
        .where(
            Notification.street_name == street.name,
            Notification.type == notification_type.value,
        )
        .order_by(Notification.created_at.desc())
    )
    return list(db.session.scalars(stmt).all())
