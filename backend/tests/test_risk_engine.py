import pytest
from app.services.risk_engine import evaluate_crop_risk
from app.schemas.weather import WeatherForecastResponse, DailyForecast

def make_test_forecast(rain_mm: float, max_temp_c: float) -> WeatherForecastResponse:
    return WeatherForecastResponse(
        location="Test Location",
        source="Test Source",
        period="2026-10-25 to 2026-10-29",
        is_demo=True,
        daily_forecasts=[
            DailyForecast(
                date="2026-10-25",
                temp_max_c=max_temp_c,
                temp_min_c=24.0,
                rainfall_mm=rain_mm,
                humidity_pct=80.0,
                weather_condition="Test Weather"
            )
        ]
    )

def test_flowering_heavy_rain_high_risk():
    """Flowering stage is highly sensitive; rain >= 40mm must trigger High risk."""
    forecast = make_test_forecast(rain_mm=55.0, max_temp_c=31.0)
    result = evaluate_crop_risk("Thanjavur", "Paddy", "Flowering", forecast)

    assert result.overall_risk == "High"
    rain_hazard = next(h for h in result.hazards if h.hazard == "Heavy Rainfall")
    assert rain_hazard.risk_level == "High"
    assert "pollen" in rain_hazard.reason_en.lower()
    assert "மகரந்த" in rain_hazard.reason_ta
    assert rain_hazard.is_demo_rule is True

def test_harvest_light_rain_medium_risk():
    """Harvest stage is sensitive to even light rain (5-15mm)."""
    forecast = make_test_forecast(rain_mm=10.0, max_temp_c=32.0)
    result = evaluate_crop_risk("Tiruchirappalli", "Paddy", "Harvest", forecast)

    rain_hazard = next(h for h in result.hazards if h.hazard == "Heavy Rainfall")
    assert rain_hazard.risk_level == "Medium"
    assert "moisture" in rain_hazard.reason_en.lower()
    assert "ஈரப்பத" in rain_hazard.reason_ta

def test_extreme_heat_high_risk():
    """Extreme heat (>39°C) in Tillering stage must trigger High heat risk."""
    forecast = make_test_forecast(rain_mm=0.0, max_temp_c=41.5)
    result = evaluate_crop_risk("Madurai", "Paddy", "Tillering", forecast)

    assert result.overall_risk == "High"
    heat_hazard = next(h for h in result.hazards if h.hazard == "Extreme Heat")
    assert heat_hazard.risk_level == "High"
    assert "tiller" in heat_hazard.reason_en.lower()
    assert "தூர்" in heat_hazard.reason_ta

def test_favorable_weather_low_risk():
    """Normal rain and moderate temperatures should result in Low risk."""
    forecast = make_test_forecast(rain_mm=5.0, max_temp_c=32.0)
    result = evaluate_crop_risk("Coimbatore", "Paddy", "Nursery", forecast)

    assert result.overall_risk == "Low"
    for h in result.hazards:
        assert h.risk_level == "Low"
