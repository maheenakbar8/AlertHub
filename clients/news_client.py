import os

import httpx
from dotenv import load_dotenv


load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


async def fetch_news():
    url = "https://gnews.io/api/v4/search"

    params = {
        "q": "earthquake OR flood OR wildfire OR cyberattack",
        "lang": "en",
        "max": 10,
        "apikey": GNEWS_API_KEY
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)

        response.raise_for_status()

        return response.json()

