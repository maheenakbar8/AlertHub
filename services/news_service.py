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

            saved_alert = await create_alert(
                db,
                alert_data
            )

            alerts.append(saved_alert)

    return alerts


def detect_event(article):
    title = article.get("title", "").lower()
    description = article.get("description", "").lower()

    # Strong keywords that should count even if they appear in the description
    strong_keywords = {
        "earthquake": [
            "earthquake",
            "earthquake hits",
            "earthquake strikes",
            "earthquake struck",
            "earthquake magnitude"
        ],
        "flood": [
            "flood",
            "flooding",
            "flash flood",
            "floods"
        ],
        "wildfire": [
            "wildfire",
            "wildfires",
            "forest fire",
            "bushfire"
        ],
        "cyberattack": [
            "cyberattack",
            "cyber attack",
            "ransomware attack",
            "ransomware"
        ]
    }

    # 1. Give the title priority.
    # A strong keyword in the title is enough to classify the article.
    for event_type, keywords in strong_keywords.items():
        for keyword in keywords:
            if keyword in title:
                return event_type

    # 2. If the title doesn't identify an event,
    # require at least TWO relevant keywords in the description.
    for event_type, keywords in strong_keywords.items():
        matches = 0

        for keyword in keywords:
            if keyword in description:
                matches += 1

        if matches >= 2:
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