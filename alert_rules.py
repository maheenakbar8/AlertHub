def detect_weather_alerts(temperature: float, wind_speed: float):
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

    return alerts