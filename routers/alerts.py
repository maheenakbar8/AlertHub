from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Alert as AlertDB
from schemas import AlertCreate, AlertResponse


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(AlertDB).all()


@router.post("/", response_model=AlertResponse)
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


@router.patch("/{alert_id}", response_model=AlertResponse)
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


@router.delete("/{alert_id}")
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