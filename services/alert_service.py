from sqlalchemy.orm import Session

from models import Alert as AlertDB
from schemas import AlertCreate


def get_all_alerts(db: Session):
    return db.query(AlertDB).all()


def create_alert(db: Session, alert: AlertCreate | dict):
    title = alert["title"] if isinstance(alert, dict) else alert.title
    severity = alert["severity"] if isinstance(alert, dict) else alert.severity
    alert_type = alert["alert_type"] if isinstance(alert, dict) else alert.alert_type

    existing_alert = (
        db.query(AlertDB)
        .filter(
            AlertDB.alert_type == alert_type,
            AlertDB.severity == severity
        )
        .first()
    )

    if existing_alert:
        return existing_alert

    new_alert = AlertDB(
        title=title,
        severity=severity,
        alert_type=alert_type
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