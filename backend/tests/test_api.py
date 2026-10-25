import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.farmer import Farmer

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    # Setup tables
    Base.metadata.create_all(bind=engine)
    yield
    # No teardown needed for sqlite in demo tests

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["demo_mode"] is True

def test_farmer_registration_and_validation():
    # Valid registration
    payload = {
        "name": "Arulmani",
        "mobile_number": "9840123456",
        "location": "Nagapattinam",
        "crop": "Paddy",
        "growth_stage": "Tillering",
        "preferred_language": "ta"
    }
    res = client.post("/api/farmers", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Arulmani"
    assert data["mobile_number"] == "+919840123456"

    # Invalid mobile number (should fail validation)
    bad_payload = payload.copy()
    bad_payload["mobile_number"] = "12345"
    res_bad = client.post("/api/farmers", json=bad_payload)
    assert res_bad.status_code == 422

def test_weather_endpoint():
    res = client.get("/api/weather/forecast?location=Thanjavur")
    assert res.status_code == 200
    data = res.json()
    assert "daily_forecasts" in data
    assert len(data["daily_forecasts"]) >= 5

def test_risk_analysis_endpoint():
    payload = {
        "location": "Thanjavur",
        "crop": "Paddy",
        "growth_stage": "Flowering"
    }
    res = client.post("/api/risk/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["crop"] == "Paddy"
    assert data["growth_stage"] == "Flowering"
    assert "hazards" in data
    assert len(data["hazards"]) == 2

def test_send_alert_and_duplicate_suppression():
    # Fetch a seeded farmer
    f_res = client.get("/api/farmers")
    assert f_res.status_code == 200
    farmers = f_res.json()
    assert len(farmers) > 0
    farmer_id = farmers[0]["id"]

    # Trigger alert
    alert_payload = {
        "farmer_id": farmer_id,
        "hazard": "Heavy Rainfall",
        "risk_level": "High",
        "force_resend": True
    }
    res = client.post("/api/alerts/send", json=alert_payload)
    assert res.status_code == 201
    alert_data = res.json()
    assert alert_data["status"] == "SIMULATED"
    assert alert_data["hazard"] == "Heavy Rainfall"

    # Attempt immediate duplicate without force_resend (should get 409 conflict)
    dup_payload = alert_payload.copy()
    dup_payload["force_resend"] = False
    dup_res = client.post("/api/alerts/send", json=dup_payload)
    assert dup_res.status_code == 409
    assert "Duplicate alert suppressed" in dup_res.json()["detail"]

    # Verify alert appears in history
    hist_res = client.get("/api/alerts/history")
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
