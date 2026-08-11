from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    title: str
    severity: str


class AlertResponse(BaseModel):
    id: int
    title: str
    severity: str

    model_config = ConfigDict(from_attributes=True)