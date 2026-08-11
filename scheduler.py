from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import SessionLocal
from services.weather_service import check_weather


scheduler = AsyncIOScheduler()


async def scheduled_weather_check():
   

    db = SessionLocal()

    try:
        await check_weather(db)
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(
        scheduled_weather_check,
        "interval",
        minutes=10,
        id="weather_check",
        replace_existing=True
    )

    scheduler.start()