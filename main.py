from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Alert(BaseModel):
    id: int
    title: str
    severity: str


alerts = [
    Alert(
        id=1,
        title="Heavy Rain Warning",
        severity="high"
    ),
    Alert(
        id=2,
        title="Road Closure",
        severity="medium"
    ),
    Alert(
        id=3,
        title="Power Outage",
        severity="low"
    )
]


@app.get("/")
def home():
    return {"message": "AlertHub is running!"}


@app.get("/alerts", response_model=list[Alert])
def get_alerts():
    return alerts