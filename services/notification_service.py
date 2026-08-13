import logging
import os

import resend
from dotenv import load_dotenv


from models import User, Alert
from services.user_service import user_wants_alert

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

logger = logging.getLogger(__name__)


async def notify_user(user: User, alert: Alert):
    if not user_wants_alert(user, alert.alert_type):
        return False

    api_key = os.getenv("RESEND_API_KEY")

    if not api_key:
        logger.error("Resend API key is not configured")
        return False

    try:
        resend.api_key = api_key

        resend.Emails.send({
            "from": "AlertHub <onboarding@resend.dev>",
            "to": [user.email],
            "subject": f"AlertHub: {alert.severity.upper()} alert - {alert.title}",
            "text": f"""AlertHub Notification

Alert: {alert.title}
Type: {alert.alert_type}
Severity: {alert.severity}

Source: {alert.source or "Unknown"}
{alert.source_url or ""}

This alert was detected by AlertHub.
"""
        })

        logger.info(
            "EMAIL SENT | user=%s | alert=%s",
            user.email,
            alert.title
        )

        return True

    except Exception:
        logger.exception(
            "EMAIL FAILED | user=%s | alert=%s",
            user.email,
            alert.title
        )

        return False


async def notify_users(db, alert: Alert):
    users = db.query(User).all()

    notified_count = 0

    for user in users:
        if await notify_user(user, alert):
            notified_count += 1

    return notified_count