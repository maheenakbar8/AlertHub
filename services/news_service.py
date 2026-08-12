import logging

from clients.news_client import fetch_news

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

async def process_news():
    news_data = await fetch_news()


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
        "source_url": article["url"]
    }