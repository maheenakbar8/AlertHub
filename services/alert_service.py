from sqlalchemy.orm import Session

from models import Alert as AlertDB
from schemas import AlertCreate


def get_all_alerts(db: Session):
    return db.query(AlertDB).all()


def create_alert(db: Session, alert: AlertCreate):
    new_alert = AlertDB(
        title=alert.title,
        severity=alert.severity
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


def get_alert_by_id(db: Session, alert_id: int):
    return (
        db.query(AlertDB)
        .filter(AlertDB.id == alert_id)
        .first()
    )


def update_alert(
    db: Session,
    alert: AlertDB,
    updated_alert: AlertCreate
):
    alert.title = updated_alert.title
    alert.severity = updated_alert.severity

    db.commit()
    db.refresh(alert)

    return alert


def delete_alert(db: Session, alert: AlertDB):
    db.delete(alert)
    db.commit()