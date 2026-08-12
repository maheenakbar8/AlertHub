from database import SessionLocal
from models import User, Alert
from services.notification_service import notify_users


db = SessionLocal()

try:
    user = db.query(User).first()
    alert = db.query(Alert).first()

    if not user:
        print("No users found.")
    elif not alert:
        print("No alerts found.")
    else:
        print(
            f"Testing notification for {user.email} "
            f"with alert: {alert.title}"
        )

        count = notify_users(db, alert)

        print(f"Users notified: {count}")

finally:
    db.close()