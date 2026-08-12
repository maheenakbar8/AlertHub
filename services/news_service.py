import logging

from clients.news_client import fetch_news
from services.alert_service import create_alert
from datetime import datetime, timezone

NEWS_KEYWORDS = {
    "earthquake": [
        "earthquake",
        "earthquake hits",
        "magnitude"
    ],
    "flood": [
        "flood",
        "flooding",
        "flash flood"
    ],
    "wildfire": [
        "wildfire",
        "forest fire",
        "bushfire"
    ],
    "cyberattack": [
        "cyberattack",
        "cyber attack",
        "ransomware"
    ]
}


logger = logging.getLogger(__name__)

async def process_news(db):
    news_data = await fetch_news()

    alerts = []

    for article in news_data.get("articles", []):
        event_type = detect_event(article)

        if event_type:
            alert_data = create_news_alert(
                article,
                event_type
            )

            saved_alert = create_alert(
                db,
                alert_data
            )

            alerts.append(saved_alert)

    return alerts


def detect_event(article):
    title = article.get("title", "")
    description = article.get("description", "")

    text = f"{title} {description}".lower()

    for event_type, keywords in NEWS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return event_type

    return None

def create_news_alert(article, event_type):
    return {
        "title": article["title"],
        "severity": "high",
        "alert_type": event_type,
        "source": article.get("source", {}).get("name"),
        "source_url": article.get("url"),
        "external_id": article.get("url"),
        "detected_at": datetime.now(timezone.utc),
    }