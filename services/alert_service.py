from sqlalchemy.orm import Session

from models import Alert as AlertDB
from schemas import AlertCreate

def get_all_alerts(
    db: Session,
    active: bool | None = None,
    severity: str | None = None,
    alert_type: str | None = None
):
    query = db.query(AlertDB)

    if active is not None:
        query = query.filter(
            AlertDB.is_active == active
        )

    if severity is not None:
        query = query.filter(
            AlertDB.severity == severity
        )

    if alert_type is not None:
        query = query.filter(
            AlertDB.alert_type == alert_type
        )

    return query.all()


def create_alert(db: Session, alert: AlertCreate | dict):
    title = alert["title"] if isinstance(alert, dict) else alert.title
    severity = alert["severity"] if isinstance(alert, dict) else alert.severity
    alert_type = alert["alert_type"] if isinstance(alert, dict) else alert.alert_type

    existing_alert = (
        db.query(AlertDB)
        .filter(
            AlertDB.alert_type == alert_type,
            AlertDB.severity == severity,
            AlertDB.is_active == True
        )
        .first()
    )

    if existing_alert:
        return existing_alert

    new_alert = AlertDB(
        title=title,
        severity=severity,
        alert_type=alert_type,
        is_active=True
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

def resolve_alert(db: Session, alert: AlertDB):
    alert.is_active = False

    db.commit()
    db.refresh(alert)

    return alert