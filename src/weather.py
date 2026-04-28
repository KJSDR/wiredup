import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather code → human description
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


class WeatherError(Exception):
    pass


def get_coordinates(city: str) -> tuple[float, float, str]:
    resp = requests.get(GEO_URL, params={"name": city, "count": 1}, timeout=10)
    data = resp.json()
    if not data.get("results"):
        raise WeatherError(f"City not found: {city}")
    r = data["results"][0]
    return r["latitude"], r["longitude"], f"{r['name']}, {r['country']}"


def get_current_weather(lat: float, lon: float) -> dict:
    resp = requests.get(
        WEATHER_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "wind_speed_unit": "kmh",
        },
        timeout=10,
    )
    if not resp.ok:
        raise WeatherError(f"API error: {resp.status_code}")
    cw = resp.json()["current_weather"]
    return {
        "temperature": cw["temperature"],
        "windspeed": cw["windspeed"],
        "description": WMO_CODES.get(cw["weathercode"], "Unknown"),
        "is_day": bool(cw["is_day"]),
    }
