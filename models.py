from sqlalchemy import Column, Integer, String, Boolean, DateTime

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