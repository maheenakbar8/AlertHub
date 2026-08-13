from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Notification
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
    return (
        db.query(Notification)
        .order_by(Notification.sent_at.desc())
        .all()
    )