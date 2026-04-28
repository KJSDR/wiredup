import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import create_app
from weather import WeatherError


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index_get_renders_form(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"city" in response.data.lower()


def test_index_post_shows_weather(client, mocker):
    mocker.patch("app.get_coordinates", return_value=(45.5, -73.5, "Montreal, Canada"))
    mocker.patch(
        "app.get_current_weather",
        return_value={"temperature": 18.5, "windspeed": 12.3, "description": "Mainly clear"},
    )
    response = client.post("/", data={"city": "Montreal"})
    assert response.status_code == 200
    assert b"Montreal" in response.data
    assert b"18.5" in response.data


def test_index_post_unknown_city_shows_error(client, mocker):
    mocker.patch("app.get_coordinates", side_effect=WeatherError("City not found"))
    response = client.post("/", data={"city": "FakeCityXYZ"})
    assert response.status_code == 200
    assert b"not found" in response.data.lower()
