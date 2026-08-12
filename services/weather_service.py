from sqlalchemy.orm import Session

from clients.weather_client import get_weather
from services import alert_service

import logging

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

    if temperature >= 40:
        alerts.append({
        "title": f"Extreme heat detected: {temperature}°C",
        "severity": "critical",
        "alert_type": "extreme_heat"
    })

    elif temperature >= 35:
        alerts.append({
        "title": f"High heat detected: {temperature}°C",
        "severity": "high",
        "alert_type": "high_heat"
    })


    if wind_speed >= 50:
        alerts.append({
        "title": f"Severe winds detected: {wind_speed} km/h",
        "severity": "critical",
        "alert_type": "severe_wind"
    })

    elif wind_speed >= 30:
        alerts.append({
        "title": f"Strong winds detected: {wind_speed} km/h",
        "severity": "high",
        "alert_type": "strong_wind"
    })

    created_alerts = []

    for alert in alerts:
        created = alert_service.create_alert(
            db,
            alert
        )

        created_alerts.append(created)

    return created_alerts