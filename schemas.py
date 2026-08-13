from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AlertCreate(BaseModel):
    title: str
    severity: str
    alert_type: str
    source: str | None = None
    source_url: str | None = None
    external_id: str | None = None
    detected_at: datetime | None = None


class AlertResponse(BaseModel):
    id: int
    title: str
    severity: str
    alert_type: str
    is_active: bool
    source: str | None = None
    source_url: str | None = None
    external_id: str | None = None
    detected_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str


class UserResponse(BaseModel):
    id: int
    email: str
    wants_weather: bool
    wants_news: bool

    model_config = ConfigDict(from_attributes=True)


class UserPreferencesUpdate(BaseModel):
    wants_weather: bool
    wants_news: bool


class NotificationAlertResponse(BaseModel):
    title: str
    severity: str
    alert_type: str
    source: str | None = None
    source_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    alert_id: int
    sent_at: datetime
    status: str
    alert: NotificationAlertResponse

    model_config = ConfigDict(from_attributes=True)