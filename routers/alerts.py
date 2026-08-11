from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import AlertCreate, AlertResponse
from services import alert_service


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
def get_alerts(
    active: bool | None = Query(default=None),
    severity: str | None = Query(default=None),
    alert_type: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return alert_service.get_all_alerts(
        db,
        active=active,
        severity=severity,
        alert_type=alert_type,
        page=page,
        limit=limit
    )
    return alert_service.get_all_alerts(
        db,
        active=active,
        severity=severity,
        alert_type=alert_type
    )


@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    return alert_service.create_alert(db, alert)


@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    updated_alert: AlertCreate,
    db: Session = Depends(get_db)
):
    alert = alert_service.get_alert_by_id(db, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert_service.update_alert(
        db,
        alert,
        updated_alert
    )


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = alert_service.get_alert_by_id(db, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert_service.delete_alert(db, alert)

    return {"message": "Alert deleted"}

@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = alert_service.get_alert_by_id(db, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert_service.resolve_alert(db, alert)