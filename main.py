from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Alert(BaseModel):
    id: int
    title: str
    severity: str


class AlertCreate(BaseModel):
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

@app.post("/alerts", response_model=Alert)
def create_alert(alert: AlertCreate):
    new_id = len(alerts) + 1

    new_alert = Alert(
        id=new_id,
        title=alert.title,
        severity=alert.severity
    )

    alerts.append(new_alert)

    return new_alert


@app.patch("/alerts/{alert_id}", response_model=Alert)
def update_alert(alert_id: int, updated_alert: AlertCreate):
    for index, alert in enumerate(alerts):
        if alert.id == alert_id:
            updated = Alert(
                id=alert_id,
                title=updated_alert.title,
                severity=updated_alert.severity
            )

            alerts[index] = updated
            return updated

    raise HTTPException(status_code=404, detail="Alert not found")


@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int):
    for index, alert in enumerate(alerts):
        if alert.id == alert_id:
            deleted_alert = alerts.pop(index)
            return {
                "message": "Alert deleted",
                "alert": deleted_alert
            }

    raise HTTPException(status_code=404, detail="Alert not found")