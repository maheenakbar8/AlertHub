from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    title: str
    severity: str
    alert_type: str


class AlertResponse(BaseModel):
    id: int
    title: str
    severity: str
    alert_type: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)