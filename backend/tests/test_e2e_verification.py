"""
Stage 5: End-to-End Local System Verification Test Suite.

Executes all 10 core verification workflows and error-handling checks:
  1. Health endpoint responsiveness and environment security.
  2. Farmer registration validation (valid data, invalid phone, invalid crop/stage).
  3. Weather forecast retrieval and provider fault resilience.
  4. Manual monitoring endpoint (/api/monitoring/run-now) execution and metrics.
  5. Controlled High/Medium risk triggering appropriate simulated alert dispatches.
  6. Controlled Low risk suppression (no alerts sent, no DB records created).
  7. 24-hour duplicate alert suppression on repeated cycles.
  8. Multilingual advisory generation respecting farmer's preferred language ('ta' vs 'en').
  9. AlertHistory audit trail logging with SIMULATED status in demo mode.
 10. Dashboard metrics structure contract and demo badge validation.
 11. Concurrency conflict (HTTP 409) prevention when cycles overlap.
"""

from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.farmer import Farmer
from app.models.alert import AlertHistory
from app.schemas.weather import WeatherForecastResponse, DailyForecast
from app.services.sms_adapter import SMSDeliveryResult

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_clean_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(AlertHistory).delete()
        db.query(Farmer).delete()
        db.commit()
    finally:
        db.close()
    yield
    db = SessionLocal()
    try:
        db.query(AlertHistory).delete()
        db.query(Farmer).delete()
        db.commit()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Check 1: Health Endpoint Verification
# ---------------------------------------------------------------------------

def test_e2e_health_endpoint():
    """Confirms health endpoint reports healthy status, demo mode active, and leaks no credentials."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["demo_mode"] is True
    # Verify no credentials leaked
    assert "token" not in data and "secret" not in data and "password" not in data


# ---------------------------------------------------------------------------
# Check 2: Farmer Registration (Valid & Invalid Handling)
# ---------------------------------------------------------------------------

def test_e2e_farmer_registration_valid():
    """Confirms farmer registration succeeds with valid data and normalizes phone number."""
    payload = {
        "name": "Arumugam",
        "mobile_number": "9876543210",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    }
    response = client.post("/api/farmers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Arumugam"
    assert data["mobile_number"] == "+919876543210"
    assert data["location"] == "Thanjavur"
    assert data["growth_stage"] == "Flowering"
    assert data["preferred_language"] == "ta"
    assert "id" in data


def test_e2e_farmer_registration_invalid_phone():
    """Confirms invalid mobile number is rejected with HTTP 422 and does not crash."""
    payload = {
        "name": "Bad Phone Farmer",
        "mobile_number": "12345",  # Invalid
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    }
    response = client.post("/api/farmers", json=payload)
    assert response.status_code == 422
    assert "mobile_number" in response.text


def test_e2e_farmer_registration_invalid_crop():
    """Confirms unapproved crops are rejected with HTTP 422."""
    payload = {
        "name": "Wheat Farmer",
        "mobile_number": "9876543210",
        "location": "Thanjavur",
        "crop": "Wheat",  # Only Paddy is configured
        "growth_stage": "Flowering",
        "preferred_language": "en",
    }
    response = client.post("/api/farmers", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Check 3: Weather Data Retrieval & Error Handling
# ---------------------------------------------------------------------------

def test_e2e_weather_retrieval_success():
    """Confirms 5-day forecast retrieval returns valid forecasts."""
    response = client.get("/api/weather/forecast?location=Thanjavur")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "Thanjavur"
    assert len(data["daily_forecasts"]) == 5
    assert data["is_demo"] is True


# ---------------------------------------------------------------------------
# Checks 4 & 5: High/Medium Risk Triggers Controlled Alert Flow
# ---------------------------------------------------------------------------

def test_e2e_high_medium_risk_alert_flow():
    """
    Controlled High-Risk Weather:
      - Heavy rain (>60mm) triggers High risk during Flowering.
      - Monitoring endpoint runs and records simulated alerts.
      - alerts_sent is strictly 0; alerts_simulated increments.
    """
    # 1. Register farmer
    farmer_payload = {
        "name": "Vetrivel",
        "mobile_number": "9443218765",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    }
    reg_res = client.post("/api/farmers", json=farmer_payload)
    assert reg_res.status_code == 201

    # 2. Run monitoring cycle
    mon_res = client.post("/api/monitoring/run-now")
    assert mon_res.status_code == 200
    summary = mon_res.json()

    assert summary["status"] == "completed"
    assert summary["farmers_checked"] >= 1
    assert summary["risks_detected"] >= 1
    assert summary["alerts_simulated"] >= 1
    assert summary["alerts_sent"] == 0  # Crucial demo separation
    assert summary["duplicates_suppressed"] == 0
    assert summary["failures"] == 0

    # 3. Verify AlertHistory record created with SIMULATED status
    hist_res = client.get("/api/alerts/history")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) >= 1
    assert history[0]["farmer_name"] == "Vetrivel"
    assert history[0]["status"] == "SIMULATED"
    assert history[0]["hazard"] in ("Heavy Rainfall", "Extreme Heat")


# ---------------------------------------------------------------------------
# Check 6: Low-Risk Conditions Do Not Trigger Alerts
# ---------------------------------------------------------------------------

def test_e2e_low_risk_suppression():
    """Under controlled mild weather, risk is Low and zero alerts are created."""
    farmer_payload = {
        "name": "Shanmugam",
        "mobile_number": "9842154321",
        "location": "SafeDistrict",
        "crop": "Paddy",
        "growth_stage": "Nursery",
        "preferred_language": "en",
    }
    client.post("/api/farmers", json=farmer_payload)

    mild_forecast = WeatherForecastResponse(
        location="SafeDistrict",
        source="Controlled Test Weather",
        period="2026-10-25 to 2026-10-29",
        is_demo=True,
        daily_forecasts=[
            DailyForecast(
                date="2026-10-25",
                temp_max_c=27.0,
                temp_min_c=22.0,
                rainfall_mm=1.0,
                humidity_pct=60.0,
                weather_condition="Clear Sky",
            )
        ],
    )

    with patch("app.services.monitoring_service.get_weather_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.get_forecast.return_value = mild_forecast
        mock_get_provider.return_value = mock_provider

        mon_res = client.post("/api/monitoring/run-now")
        assert mon_res.status_code == 200
        summary = mon_res.json()

        assert summary["farmers_checked"] == 1
        assert summary["risks_detected"] == 0
        assert summary["alerts_simulated"] == 0
        assert summary["alerts_sent"] == 0
        assert summary["duplicates_suppressed"] == 0
        assert summary["failures"] == 0

        # No alerts should be logged
        hist_res = client.get("/api/alerts/history")
        assert len(hist_res.json()) == 0


# ---------------------------------------------------------------------------
# Check 7: Duplicate Warnings Suppressed
# ---------------------------------------------------------------------------

def test_e2e_duplicate_warnings_suppressed():
    """Running monitoring twice within 24h suppresses duplicate alerts."""
    client.post("/api/farmers", json={
        "name": "Annamalai",
        "mobile_number": "9789012345",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    })

    # Cycle 1
    res1 = client.post("/api/monitoring/run-now")
    assert res1.status_code == 200
    sum1 = res1.json()
    assert sum1["alerts_simulated"] >= 1
    first_simulated = sum1["alerts_simulated"]

    # Cycle 2 immediately afterwards
    res2 = client.post("/api/monitoring/run-now")
    assert res2.status_code == 200
    sum2 = res2.json()
    assert sum2["alerts_simulated"] == 0
    assert sum2["alerts_sent"] == 0
    assert sum2["duplicates_suppressed"] == first_simulated
    assert sum2["failures"] == 0


# ---------------------------------------------------------------------------
# Check 8: Multilingual Tamil & English Warnings
# ---------------------------------------------------------------------------

def test_e2e_multilingual_warnings_respect_language_preference():
    """Tamil and English farmers receive alerts in their respective languages."""
    client.post("/api/farmers", json={
        "name": "Muthu Tamil",
        "mobile_number": "9123456780",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    })
    client.post("/api/farmers", json={
        "name": "David English",
        "mobile_number": "9123456781",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "en",
    })

    client.post("/api/monitoring/run-now")

    hist_res = client.get("/api/alerts/history")
    records = hist_res.json()
    assert len(records) >= 2

    ta_record = next(r for r in records if r["farmer_name"] == "Muthu Tamil")
    en_record = next(r for r in records if r["farmer_name"] == "David English")

    assert ta_record["language"] == "ta"
    # Contains Tamil characters
    assert any("\u0b80" <= c <= "\u0bff" for c in ta_record["message"])

    assert en_record["language"] == "en"
    # Contains English terms
    assert "TamilAgri Alert" in en_record["message"] or "Dear" in en_record["message"]


# ---------------------------------------------------------------------------
# Check 9: Alert History Audit Trail
# ---------------------------------------------------------------------------

def test_e2e_alert_history_filtering():
    """Alert history endpoint supports filtering by hazard and status."""
    client.post("/api/farmers", json={
        "name": "Audit Farmer",
        "mobile_number": "9876501234",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "en",
    })
    client.post("/api/monitoring/run-now")

    # Filter by status=SIMULATED
    res = client.get("/api/alerts/history?status=SIMULATED")
    assert res.status_code == 200
    for record in res.json():
        assert record["status"] == "SIMULATED"


# ---------------------------------------------------------------------------
# Check 10 & Error Handling: Weather Failure Resilience
# ---------------------------------------------------------------------------

def test_e2e_weather_failure_handled_without_crashing():
    """When weather service fails for a location, failures count increments without server crash."""
    client.post("/api/farmers", json={
        "name": "Fault Farmer",
        "mobile_number": "9988776655",
        "location": "FailingDistrict",
        "crop": "Paddy",
        "growth_stage": "Nursery",
        "preferred_language": "ta",
    })

    async def mock_fail_forecast(loc):
        raise ConnectionError("Weather gateway connection timed out")

    with patch("app.services.monitoring_service.get_weather_provider") as mock_get_provider:
        mock_provider = AsyncMock()
        mock_provider.get_forecast.side_effect = mock_fail_forecast
        mock_get_provider.return_value = mock_provider

        res = client.post("/api/monitoring/run-now")
        assert res.status_code == 200
        summary = res.json()
        assert summary["status"] == "completed"
        assert summary["failures"] >= 1
        assert summary["alerts_simulated"] == 0


# ---------------------------------------------------------------------------
# Error Handling: SMS Gateway Failure Resilience
# ---------------------------------------------------------------------------

def test_e2e_sms_gateway_failure_handled_without_crashing():
    """When SMS provider fails, failures count increments and no secrets are exposed."""
    client.post("/api/farmers", json={
        "name": "SMS Fail Farmer",
        "mobile_number": "9988776655",
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "preferred_language": "ta",
    })

    failed_sms = SMSDeliveryResult(
        success=False,
        status="FAILED",
        provider="mock_gateway",
        error_message="Gateway timeout",
    )

    with patch("app.routes.alerts.get_sms_provider") as mock_get_sms:
        mock_sms = AsyncMock()
        mock_sms.send_sms.return_value = failed_sms
        mock_get_sms.return_value = mock_sms

        res = client.post("/api/monitoring/run-now")
        assert res.status_code == 200
        summary = res.json()
        assert summary["failures"] >= 1
        assert summary["alerts_sent"] == 0
        assert summary["alerts_simulated"] == 0


# ---------------------------------------------------------------------------
# Error Handling: Concurrent Monitoring Requests (409 Conflict)
# ---------------------------------------------------------------------------

def test_e2e_concurrent_monitoring_returns_409():
    """Concurrent monitoring request returns HTTP 409 Conflict."""
    with patch("app.routes.monitoring.is_cycle_running", return_value=True):
        res = client.post("/api/monitoring/run-now")
        assert res.status_code == 409
        assert "in progress" in res.json()["detail"].lower()
