from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Alert as AlertDB


Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------- Database dependency ----------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic models ----------

class AlertCreate(BaseModel):
    title: str
    severity: str


class AlertResponse(BaseModel):
    id: int
    title: str
    severity: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Routes ----------

@app.get("/")
def home():
    return {"message": "AlertHub is running!"}


@app.get("/alerts", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(AlertDB).all()


@app.post("/alerts", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    new_alert = AlertDB(
        title=alert.title,
        severity=alert.severity
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@app.patch("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    updated_alert: AlertCreate,
    db: Session = Depends(get_db)
):
    alert = db.query(AlertDB).filter(AlertDB.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.title = updated_alert.title
    alert.severity = updated_alert.severity

    db.commit()
    db.refresh(alert)

    return alert


@app.delete("/alerts/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(AlertDB).filter(AlertDB.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted"}