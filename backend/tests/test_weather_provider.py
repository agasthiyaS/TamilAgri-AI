import pytest
from unittest.mock import patch, AsyncMock
import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.weather_adapter import (
    get_weather_provider,
    OpenMeteoWeatherProvider,
    DemoWeatherProvider,
)
from app.schemas.weather import WeatherForecastResponse, DailyForecast

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_settings():
    original_provider = settings.WEATHER_PROVIDER
    original_demo = settings.DEMO_MODE
    yield
    settings.WEATHER_PROVIDER = original_provider
    settings.DEMO_MODE = original_demo

def test_get_weather_provider_factory():
    """Verify factory returns OpenMeteoWeatherProvider when configured, even if DEMO_MODE is true."""
    settings.WEATHER_PROVIDER = "open_meteo"
    settings.DEMO_MODE = True
    provider = get_weather_provider()
    assert isinstance(provider, OpenMeteoWeatherProvider)

    settings.WEATHER_PROVIDER = "demo"
    provider_demo = get_weather_provider()
    assert isinstance(provider_demo, DemoWeatherProvider)

def test_weather_forecast_empty_location():
    """GET /api/weather/forecast with empty location should return 400 Bad Request."""
    res = client.get("/api/weather/forecast?location=   ")
    assert res.status_code == 400
    assert "cannot be empty" in res.json()["detail"]

def test_risk_analyze_invalid_forecast():
    """POST /api/risk/analyze with empty daily_forecasts should return 400."""
    empty_forecast = {
        "location": "Thanjavur",
        "source": "Empty Test",
        "period": "None",
        "is_demo": True,
        "daily_forecasts": []
    }
    res = client.post("/api/risk/analyze", json={
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "forecast_data": empty_forecast
    })
    assert res.status_code == 400
    assert "no daily forecasts available" in res.json()["detail"]

def test_open_meteo_timeout_error_handling():
    """Open-Meteo timeout should raise HTTP 503 rather than returning fake demo data or 500."""
    settings.WEATHER_PROVIDER = "open_meteo"
    with patch("httpx.AsyncClient.get", side_effect=httpx.ConnectTimeout("Connection timed out")):
        res = client.get("/api/weather/forecast?location=Thanjavur")
        assert res.status_code == 503
        assert "timed out" in res.json()["detail"].lower()

def test_open_meteo_server_error_handling():
    """Open-Meteo 500 status should raise HTTP 502 rather than returning fake demo data."""
    settings.WEATHER_PROVIDER = "open_meteo"
    with patch("httpx.AsyncClient.get", return_value=httpx.Response(500, content=b"Server Error")):
        res = client.get("/api/weather/forecast?location=Thanjavur")
        assert res.status_code == 502
        assert "Open-Meteo weather API returned error HTTP 500" in res.json()["detail"]

def test_open_meteo_empty_forecast_data():
    """Open-Meteo 200 with empty daily data should raise HTTP 502 rather than list index crash."""
    settings.WEATHER_PROVIDER = "open_meteo"
    mock_empty = httpx.Response(
        200,
        json={"daily": {"time": [], "temperature_2m_max": [], "temperature_2m_min": [], "precipitation_sum": []}}
    )
    with patch("httpx.AsyncClient.get", return_value=mock_empty):
        res = client.get("/api/weather/forecast?location=Thanjavur")
        assert res.status_code == 502
        assert "No forecast data returned" in res.json()["detail"]

def test_risk_analyze_with_open_meteo_success():
    """POST /api/risk/analyze should succeed with open_meteo provider."""
    settings.WEATHER_PROVIDER = "open_meteo"
    mock_data = {
        "daily": {
            "time": ["2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29"],
            "temperature_2m_max": [32.0, 33.0, 34.0, 32.5, 31.0],
            "temperature_2m_min": [24.0, 24.5, 25.0, 24.0, 23.5],
            "precipitation_sum": [45.0, 10.0, 2.0, 0.0, 0.0]
        }
    }
    with patch("httpx.AsyncClient.get", return_value=httpx.Response(200, json=mock_data)):
        res = client.post("/api/risk/analyze", json={
            "location": "Thanjavur",
            "crop": "Paddy",
            "growth_stage": "Flowering"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["overall_risk"] == "High"
        assert data["forecast_source"] == "Open-Meteo Live API (Free Tier)"
        assert len(data["hazards"]) == 2
