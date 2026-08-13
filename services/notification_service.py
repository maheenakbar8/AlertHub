import logging
import os

from dotenv import load_dotenv

load_dotenv()

from datetime import datetime, timezone
from email.message import EmailMessage

import aiosmtplib

from models import User, Alert, Notification
from services.user_service import user_wants_alert

logger = logging.getLogger(__name__)

EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "true").lower() == "true"


async def notify_user(db, user: User, alert: Alert):
    if not user_wants_alert(user, alert.alert_type):
        return False

    if not EMAIL_ENABLED:
        notification = Notification(
            user_id=user.id,
            alert_id=alert.id,
            sent_at=datetime.now(timezone.utc),
            status="mocked"
        )

        db.add(notification)
        db.commit()

        logger.info(
            "EMAIL MOCKED | user=%s | alert=%s",
            user.email,
            alert.title
        )

        return True

    email_address = os.getenv("EMAIL_ADDRESS")
    api_key = os.getenv("RESEND_API_KEY")

    if not email_address or not api_key:
        logger.error("Email credentials are not configured")
        return False

    message = EmailMessage()

    message["From"] = email_address
    message["To"] = user.email
    message["Subject"] = (
        f"AlertHub: {alert.severity.upper()} alert - {alert.title}"
    )

    message.set_content(
        f"""AlertHub Notification

Alert: {alert.title}
Type: {alert.alert_type}
Severity: {alert.severity}

Source: {alert.source or "Unknown"}
{alert.source_url or ""}

This alert was detected by AlertHub.
"""
    )

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.resend.com",
            port=587,
            start_tls=True,
            username="resend",
            password=api_key,
        )

        notification = Notification(
            user_id=user.id,
            alert_id=alert.id,
            sent_at=datetime.now(timezone.utc),
            status="sent"
        )

        db.add(notification)
        db.commit()

        logger.info(
            "EMAIL SENT | user=%s | alert=%s",
            user.email,
            alert.title
        )

        return True

    except Exception:
        db.rollback()

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
        if await notify_user(db, user, alert):
            notified_count += 1

    return notified_count