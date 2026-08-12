import logging

from models import User, Alert
from services.user_service import user_wants_alert

logger = logging.getLogger(__name__)


def notify_user(user: User, alert: Alert):
    if not user_wants_alert(user, alert.alert_type):
        return False

    logger.info(
        "ALERT NOTIFICATION | user=%s | alert=%s | severity=%s | type=%s",
        user.email,
        alert.title,
        alert.severity,
        alert.alert_type
    )

    return True


def notify_users(db, alert: Alert):
    users = db.query(User).all()

    notified_count = 0

    for user in users:
        if notify_user(user, alert):
            notified_count += 1

    return notified_count