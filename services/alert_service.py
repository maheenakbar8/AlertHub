from sqlalchemy.orm import Session

from models import Alert as AlertDB
from schemas import AlertCreate
from services.notification_service import notify_users

def get_all_alerts(
    db: Session,
    active: bool | None = None,
    severity: str | None = None,
    alert_type: str | None = None,
    page: int = 1,
    limit: int = 10
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

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


async def create_alert(db: Session, alert: AlertCreate | dict):
    if isinstance(alert, dict):
        title = alert["title"]
        severity = alert["severity"]
        alert_type = alert["alert_type"]
        source = alert.get("source")
        source_url = alert.get("source_url")
        external_id = alert.get("external_id")
        detected_at = alert.get("detected_at")
    else:
        title = alert.title
        severity = alert.severity
        alert_type = alert.alert_type
        source = alert.source
        source_url = alert.source_url
        external_id = alert.external_id
        detected_at = alert.detected_at

    # Check whether this exact external item already exists
    if external_id:
        existing_alert = (
            db.query(AlertDB)
            .filter(AlertDB.external_id == external_id)
            .first()
        )

        if existing_alert:
            return existing_alert

    new_alert = AlertDB(
        title=title,
        severity=severity,
        alert_type=alert_type,
        is_active=True,
        source=source,
        source_url=source_url,
        external_id=external_id,
        detected_at=detected_at
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    await notify_users(db, new_alert)

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