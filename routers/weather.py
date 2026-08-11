from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from services.weather_service import check_weather


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/check")
async def check_weather_endpoint(
    db: Session = Depends(get_db)
):
    return await check_weather(db)