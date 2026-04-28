import pytest
from unittest.mock import patch, Mock
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather import get_coordinates, get_current_weather, WeatherError


GEO_RESPONSE = {
    "results": [{"name": "Montreal", "latitude": 45.5017, "longitude": -73.5673, "country": "Canada"}]
}

WEATHER_RESPONSE = {
    "current_weather": {
        "temperature": 18.5,
        "windspeed": 12.3,
        "weathercode": 1,
        "is_day": 1,
    }
}


def test_get_coordinates_returns_lat_lon(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        json=GEO_RESPONSE,
    )
    lat, lon, name = get_coordinates("Montreal")
    assert lat == 45.5017
    assert lon == -73.5673
    assert name == "Montreal, Canada"


def test_get_coordinates_unknown_city_raises(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        json={},
    )
    with pytest.raises(WeatherError, match="not found"):
        get_coordinates("FakeCityXYZ")


def test_get_current_weather_returns_data(requests_mock):
    requests_mock.get(
        "https://api.open-meteo.com/v1/forecast",
        json=WEATHER_RESPONSE,
    )
    data = get_current_weather(45.5017, -73.5673)
    assert data["temperature"] == 18.5
    assert data["windspeed"] == 12.3
    assert "description" in data


def test_get_current_weather_api_failure_raises(requests_mock):
    requests_mock.get(
        "https://api.open-meteo.com/v1/forecast",
        status_code=500,
    )
    with pytest.raises(WeatherError, match="API error"):
        get_current_weather(45.5017, -73.5673)
