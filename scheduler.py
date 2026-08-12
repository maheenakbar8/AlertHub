import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import SessionLocal
from services.weather_service import check_weather
from services.news_service import process_news
from datetime import datetime


logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()


async def scheduled_weather_check():
    logger.info("Running scheduled weather check")

    db = SessionLocal()

    try:
        await check_weather(db)
        logger.info("Weather check completed successfully")

    except Exception:
        logger.exception("Weather check failed")

    finally:
        db.close()


async def scheduled_news_check():
    logger.info("Running scheduled news check")

    db = SessionLocal()

    try:
        alerts = await process_news(db)

        logger.info(
            f"News check completed successfully: {len(alerts)} alerts processed"
        )

    except Exception:
        logger.exception("News check failed")

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

    scheduler.add_job(
    scheduled_news_check,
    "interval",
    minutes=10,
    id="news_check",
    replace_existing=True,
    next_run_time=datetime.now(),
)
    scheduler.start() 