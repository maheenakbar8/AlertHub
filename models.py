from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint

from database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    alert_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    source = Column(String, nullable=True)

    source_url = Column(String, nullable=True)

    external_id = Column(String, nullable=True)

    detected_at = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)

    wants_weather = Column(Boolean, default=True, nullable=False)
    wants_news = Column(Boolean, default=True, nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    alert_id = Column(Integer, nullable=False)

    sent_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="sent")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "alert_id",
            name="uq_user_alert_notification"
        ),
    )