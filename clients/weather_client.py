import httpx


async def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 31.5204,
        "longitude": 74.3587,
        "current": "temperature_2m,wind_speed_10m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    return response.json()