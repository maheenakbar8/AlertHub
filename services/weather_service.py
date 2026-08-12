from sqlalchemy.orm import Session

from clients.weather_client import get_weather
from services import alert_service

import logging
from alert_rules import detect_weather_alerts

logger = logging.getLogger(__name__)


async def check_weather(db: Session):
    weather = await get_weather()

    current = weather["current"]

    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]

    logger.info(
    f"Weather data: {temperature}°C, wind {wind_speed} km/h"
)

    alerts = []

    alerts = detect_weather_alerts(
    temperature,
    wind_speed
)

    created_alerts = []

    for alert in alerts:
        created = alert_service.create_alert(
            db,
            alert
        )

        created_alerts.append(created)

    return created_alerts