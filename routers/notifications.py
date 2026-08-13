from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Notification, Alert
from schemas import NotificationResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db)
):
    results = (
        db.query(Notification, Alert)
        .join(Alert, Notification.alert_id == Alert.id)
        .order_by(Notification.sent_at.desc())
        .all()
    )

    return [
        {
            "id": notification.id,
            "user_id": notification.user_id,
            "alert_id": notification.alert_id,
            "sent_at": notification.sent_at,
            "status": notification.status,
            "alert": alert
        }
        for notification, alert in results
    ]