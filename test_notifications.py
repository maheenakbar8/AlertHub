import asyncio

from database import SessionLocal
from models import Alert
from services.notification_service import notify_users


async def main():
    db = SessionLocal()

    try:
        alert = (
            db.query(Alert)
            .filter(Alert.external_id.like("test-%"))
            .order_by(Alert.id.desc())
            .first()
        )

        if alert is None:
            print("No test alert found.")
            return

        print(f"Testing notification for: {alert.title}")

        notified = await notify_users(db, alert)

        print(f"Users notified: {notified}")

    finally:
        db.close()


asyncio.run(main())