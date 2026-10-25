"""
Stage 1 tests: verify _build_and_dispatch_alert() helper behaviour
independently of HTTP routing.

These tests call the helper directly (not via HTTP) to prove:
  - The helper always returns an AlertDispatchResult (never raises).
  - Duplicate suppression returns skip_reason="DUPLICATE" without a DB write.
  - force_resend=True bypasses the duplicate guard.
  - A successful dispatch sets was_sent=True with a fully populated AlertHistory.
  - SMS status is always "SIMULATED" in demo mode.
  - The API route still surfaces HTTP 201 / 409 / 404 exactly as before.

Helper-level tests are async def (driven by anyio, already installed) so
they work correctly on Python 3.14+ without relying on get_event_loop().
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.farmer import Farmer
from app.models.alert import AlertHistory
from app.routes.alerts import _build_and_dispatch_alert, AlertDispatchResult


# ---------------------------------------------------------------------------
# Shared HTTP test client (matches existing test_api.py pattern)
# ---------------------------------------------------------------------------
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield


# ---------------------------------------------------------------------------
# Sync helpers — DB fixture creation and counting
# ---------------------------------------------------------------------------

def _make_farmer(**kwargs) -> Farmer:
    """Creates and persists a minimal farmer fixture."""
    db = SessionLocal()
    try:
        defaults = dict(
            name="Test Farmer",
            mobile_number="+919999900000",
            location="Thanjavur",
            crop="Paddy",
            growth_stage="Flowering",
            preferred_language="ta",
        )
        defaults.update(kwargs)
        farmer = Farmer(**defaults)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer
    finally:
        db.close()


def _count_alert_history(farmer_id: int, hazard: str) -> int:
    db = SessionLocal()
    try:
        return (
            db.query(AlertHistory)
            .filter(
                AlertHistory.farmer_id == farmer_id,
                AlertHistory.hazard == hazard,
            )
            .count()
        )
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Helper-level tests — async def, driven by anyio
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_returns_alert_dispatch_result_type():
    """Helper always returns an AlertDispatchResult, never raises."""
    farmer = _make_farmer(mobile_number="+919999900001")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()
    assert isinstance(result, AlertDispatchResult)


@pytest.mark.anyio
async def test_successful_dispatch_was_sent_true():
    """A fresh alert with no prior history is dispatched and recorded."""
    farmer = _make_farmer(mobile_number="+919999900002")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Extreme Heat",
            risk_level="Medium",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.was_sent is True
    assert result.skip_reason is None
    assert result.alert_record is not None
    assert result.alert_record.hazard == "Extreme Heat"
    assert result.alert_record.risk_level == "Medium"


@pytest.mark.anyio
async def test_sms_is_simulated_in_demo_mode():
    """Demo mode must never produce DELIVERED — status must be SIMULATED."""
    farmer = _make_farmer(mobile_number="+919999900003")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.alert_record.status == "SIMULATED"
    assert result.alert_record.provider == "demo"


@pytest.mark.anyio
async def test_alert_history_record_written_to_db():
    """After dispatch the AlertHistory row must be readable from the DB."""
    farmer = _make_farmer(mobile_number="+919999900004")
    db = SessionLocal()
    try:
        await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()

    assert _count_alert_history(farmer.id, "Heavy Rainfall") == 1


@pytest.mark.anyio
async def test_duplicate_returns_skip_reason_not_exception():
    """Second call within 24 h must return skip_reason='DUPLICATE', not raise."""
    farmer = _make_farmer(mobile_number="+919999900005")
    db = SessionLocal()
    try:
        # First dispatch
        await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
        # Second dispatch — same hazard + risk_level, force_resend=False
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=False,
        )
    finally:
        db.close()

    assert result.skip_reason == "DUPLICATE"
    assert result.was_sent is False
    assert result.alert_record is None
    # Only one record should exist (from the first dispatch)
    assert _count_alert_history(farmer.id, "Heavy Rainfall") == 1


@pytest.mark.anyio
async def test_force_resend_bypasses_duplicate_check():
    """force_resend=True must dispatch even when a recent record exists."""
    farmer = _make_farmer(mobile_number="+919999900006")
    db = SessionLocal()
    try:
        await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Extreme Heat",
            risk_level="High",
            force_resend=True,
        )
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Extreme Heat",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.was_sent is True
    assert result.skip_reason is None
    assert _count_alert_history(farmer.id, "Extreme Heat") == 2


@pytest.mark.anyio
async def test_tamil_language_preference_respected():
    """Farmer with preferred_language='ta' gets a Tamil-script message."""
    farmer = _make_farmer(mobile_number="+919999900007", preferred_language="ta")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.alert_record.language == "ta"
    assert "தமிழ் அக்ரி" in result.alert_record.message


@pytest.mark.anyio
async def test_english_language_preference_respected():
    """Farmer with preferred_language='en' gets an English message."""
    farmer = _make_farmer(
        mobile_number="+919999900008",
        preferred_language="en",
        location="Tiruchirappalli",
    )
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.alert_record.language == "en"
    assert "TamilAgri" in result.alert_record.message


@pytest.mark.anyio
async def test_caller_supplied_reason_precaution_used_directly():
    """When reason and precaution are supplied, they appear in the final SMS
    without any forecast fetch."""
    farmer = _make_farmer(mobile_number="+919999900009", preferred_language="en")
    custom_precaution = "Evacuate low-lying fields immediately."
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            force_resend=True,
            reason="Test reason for flood risk.",
            precaution=custom_precaution,
        )
    finally:
        db.close()

    assert result.was_sent is True
    assert custom_precaution in result.alert_record.message


@pytest.mark.anyio
async def test_custom_message_used_verbatim():
    """A custom_message bypasses all generation logic and is stored as-is."""
    farmer = _make_farmer(mobile_number="+919999900010")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Heavy Rainfall",
            risk_level="High",
            custom_message="Verbatim custom alert message.",
            force_resend=True,
        )
    finally:
        db.close()

    assert result.alert_record.message == "Verbatim custom alert message."


@pytest.mark.anyio
async def test_all_alert_history_fields_populated():
    """Every AlertHistory column the API contract exposes must be set."""
    farmer = _make_farmer(mobile_number="+919999900011")
    db = SessionLocal()
    try:
        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard="Extreme Heat",
            risk_level="Medium",
            force_resend=True,
        )
    finally:
        db.close()

    rec = result.alert_record
    assert rec.farmer_id == farmer.id
    assert rec.farmer_name == farmer.name
    assert rec.mobile_number == farmer.mobile_number
    assert rec.location == farmer.location
    assert rec.crop == farmer.crop
    assert rec.growth_stage == farmer.growth_stage
    assert rec.hazard == "Extreme Heat"
    assert rec.risk_level == "Medium"
    assert rec.language == farmer.preferred_language
    assert rec.message          # non-empty
    assert rec.status           # "SIMULATED" / "DELIVERED" / "FAILED"
    assert rec.provider         # "demo" etc.
    assert rec.sent_at is not None


# ---------------------------------------------------------------------------
# API-level regression tests — HTTP contract must be unchanged
# ---------------------------------------------------------------------------

def test_send_alert_returns_201_on_success():
    farmer_id = client.get("/api/farmers").json()[0]["id"]
    res = client.post(
        "/api/alerts/send",
        json={"farmer_id": farmer_id, "hazard": "Heavy Rainfall",
              "risk_level": "High", "force_resend": True},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "SIMULATED"
    assert data["hazard"] == "Heavy Rainfall"


def test_send_alert_returns_409_on_duplicate():
    farmer_id = client.get("/api/farmers").json()[0]["id"]
    payload = {"farmer_id": farmer_id, "hazard": "Extreme Heat",
               "risk_level": "High", "force_resend": True}
    client.post("/api/alerts/send", json=payload)
    payload["force_resend"] = False
    dup_res = client.post("/api/alerts/send", json=payload)
    assert dup_res.status_code == 409
    assert "Duplicate alert suppressed" in dup_res.json()["detail"]


def test_send_alert_returns_404_for_unknown_farmer():
    res = client.post(
        "/api/alerts/send",
        json={"farmer_id": 99999, "hazard": "Heavy Rainfall", "risk_level": "High"},
    )
    assert res.status_code == 404


def test_force_resend_overrides_duplicate_at_api_level():
    farmer_id = client.get("/api/farmers").json()[0]["id"]
    payload = {"farmer_id": farmer_id, "hazard": "Heavy Rainfall",
               "risk_level": "Medium", "force_resend": True}
    r1 = client.post("/api/alerts/send", json=payload)
    r2 = client.post("/api/alerts/send", json=payload)
    assert r1.status_code == 201
    assert r2.status_code == 201


def test_alert_history_populated_after_send():
    farmer_id = client.get("/api/farmers").json()[0]["id"]
    client.post(
        "/api/alerts/send",
        json={"farmer_id": farmer_id, "hazard": "Extreme Heat",
              "risk_level": "Medium", "force_resend": True},
    )
    hist = client.get("/api/alerts/history").json()
    assert len(hist) >= 1
    assert any(h["hazard"] == "Extreme Heat" for h in hist)
