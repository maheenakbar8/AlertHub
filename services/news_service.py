import logging

from clients.news_client import fetch_news
from services.alert_service import create_alert
from datetime import datetime, timezone

NEWS_KEYWORDS = {
    "earthquake": [
        "earthquake",
        "earthquake hits",
        "earthquake struck",
        "earthquake strikes",
        "earthquake rocks",
        "earthquake devastates",
        "earthquake kills",
        "earthquake victims",
        "earthquake survivors",
        "earthquake rescue",
        "seismic"
    ],
    "flood": [
    "flood",
    "flooding",
    "flash flood",
    "flash flooding",
    "flood emergency",
    "flood warning",
    "floods threaten",
    "flood victims",
    "flood rescue",
    "flood evacuation",
    "heavy rain",
    "heavy rainfall",
    "submerged",
    "submerges",
    "inundated",
    "waterlogging"
],
       
    
    "wildfire": [
        "wildfire",
        "wildfires",
        "forest fire",
        "forest fires",
        "bushfire",
        "wildfire evacuation",
        "wildfire emergency",
        "wildfire spreads",
        "wildfire destroys"
    ],
    "cyberattack": [
        "cyberattack",
        "cyber attack",
        "ransomware attack",
        "ransomware",
        "cyber breach",
        "data breach",
        "hacking attack"
    ]
}

EXCLUDED_TERMS = [
    "video game",
    "game",
    "gaming",
    "market price",
    "legend items",
    "item prices",
    "fantasy",
]

DISASTER_CONTEXT = [
    "emergency",
    "warning",
    "evacuation",
    "evacuated",
    "rescue",
    "rescued",
    "victims",
    "killed",
    "injured",
    "destroyed",
    "damage",
    "damaged",
    "disaster",
    "devastating",
    "devastation",
    "threat",
    "threatens",
    "authorities",
    "officials",
    "survivors",
    "survival",
    "homes",
    "residents",
    "fatalities",
    "death toll",
    "submerged",
    "submerges",
    "inundated",
    "waterlogging"
]


FLOOD_EXCLUDED_PHRASES = [
    "flood in",
    "flood of",
    "floods of",
    "flooded with",
    "flood of tributes",
    "flood of messages",
    "flood of support",
    "flood of criticism",
]


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
    title = article.get("title", "")
    description = article.get("description", "")

    text = f"{title} {description}".lower()

    # Ignore clearly irrelevant uses of disaster keywords
    if any(term in text for term in EXCLUDED_TERMS):
        return None

    for event_type, keywords in NEWS_KEYWORDS.items():

        # Check whether this event is mentioned
        if not any(keyword in text for keyword in keywords):
            continue

        # Cyberattacks are already specific enough
        if event_type == "cyberattack":
            return event_type

        # Wildfire terminology is also highly specific
        if event_type == "wildfire":
            return event_type

        # Earthquake terminology is highly specific
        if event_type == "earthquake":
            return event_type

        # Flood needs extra context because "flood" can be metaphorical
        if event_type == "flood":
            if any(keyword in text for keyword in DISASTER_CONTEXT):
                return event_type

    return None

def create_news_alert(article, event_type):
    return {
        "title": article["title"],
        "severity": determine_severity(article, event_type),
        "alert_type": event_type,
        "source": article.get("source", {}).get("name"),
        "source_url": article.get("url"),
        "external_id": article.get("url"),
        "detected_at": datetime.now(timezone.utc),
    }


def determine_severity(article, event_type):
    title = article.get("title", "").lower()
    description = article.get("description", "").lower()

    text = f"{title} {description}"

    critical_terms = [
        "death",
        "deaths",
        "killed",
        "dead",
        "evacuation",
        "evacuated",
        "emergency",
        "devastating",
        "catastrophic",
        "major",
        "massive",
        "life-threatening"
    ]

    if any(term in text for term in critical_terms):
        return "critical"

    if event_type == "earthquake":
        # Try to detect earthquake magnitude
        import re

        match = re.search(r"magnitude\s+(\d+(?:\.\d+)?)", text)

        if match:
            magnitude = float(match.group(1))

            if magnitude >= 7:
                return "critical"
            elif magnitude >= 5:
                return "high"
            elif magnitude >= 3:
                return "medium"
            else:
                return "low"

    return "medium"