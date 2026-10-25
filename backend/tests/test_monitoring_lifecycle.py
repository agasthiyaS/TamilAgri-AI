"""
Stage 3 tests: verify FastAPI lifecycle integration and manual monitoring endpoint.

These tests prove:
  1. The application starts without creating a scheduler task when SCHEDULER_ENABLED=false.
  2. The scheduler task is started when SCHEDULER_ENABLED=true.
  3. Lifespan shutdown cancels and awaits the scheduler task cleanly.
  4. POST /api/monitoring/run-now returns the monitoring cycle summary.
  5. A concurrent run request is safely rejected with HTTP 409 Conflict.
  6. Existing API routes continue to work normally.
  7. Demo SMS remains strictly SIMULATED and is never counted as alerts_sent.
"""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from app.main import app, lifespan, get_scheduler_task
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models.farmer import Farmer
from app.models.alert import AlertHistory
from app.services.monitoring_service import run_monitoring_cycle, is_cycle_running

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
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


def _create_sample_farmer(name: str = "Test Farmer", location: str = "Thanjavur"):
    db = SessionLocal()
    try:
        farmer = Farmer(
            name=name,
            mobile_number="+919876543210",
            location=location,
            crop="Paddy",
            growth_stage="Flowering",
            preferred_language="ta",
        )
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer
    finally:
        db.close()


# ---------------------------------------------------------------------------
# 1, 2, 3: Lifespan tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_lifespan_starts_without_scheduler_when_disabled():
    """Application starts without creating a background task when SCHEDULER_ENABLED=false."""
    with patch.object(settings, "SCHEDULER_ENABLED", False):
        async with lifespan(app):
            task = get_scheduler_task()
            assert task is None


@pytest.mark.anyio
async def test_lifespan_starts_and_stops_scheduler_when_enabled():
    """
    When SCHEDULER_ENABLED=true:
      - Lifespan starts the monitoring task.
      - Shutdown cleanly cancels and awaits it.
    """
    with patch.object(settings, "SCHEDULER_ENABLED", True):
        task_ref = None
        async with lifespan(app):
            task_ref = get_scheduler_task()
            assert task_ref is not None
            assert not task_ref.done()

        # After exiting lifespan context manager, shutdown code has run:
        assert task_ref.done() or task_ref.cancelled()
        assert get_scheduler_task() is None


# ---------------------------------------------------------------------------
# 4: Manual monitoring endpoint returns summary
# ---------------------------------------------------------------------------

def test_manual_monitoring_run_now_endpoint_returns_summary():
    """POST /api/monitoring/run-now executes a cycle and returns the expected summary structure."""
    _create_sample_farmer("Raman", "Thanjavur")

    response = client.post("/api/monitoring/run-now")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"
    assert data["farmers_checked"] >= 1
    assert data["risks_detected"] >= 1
    assert data["alerts_simulated"] >= 1
    assert data["alerts_sent"] == 0  # Strict demo mode separation
    assert data["duplicates_suppressed"] == 0
    assert data["failures"] == 0
    assert "cycle_duration_seconds" in data


# ---------------------------------------------------------------------------
# 5: Concurrent run request rejected safely with HTTP 409
# ---------------------------------------------------------------------------

def test_concurrent_manual_run_returns_409_conflict():
    """If a cycle is already active, POST /api/monitoring/run-now returns HTTP 409 Conflict."""
    with patch("app.routes.monitoring.is_cycle_running", return_value=True):
        response = client.post("/api/monitoring/run-now")
        assert response.status_code == 409
        assert "in progress" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# 6: Existing API routes continue to work normally
# ---------------------------------------------------------------------------

def test_existing_api_routes_continue_to_work():
    """Regression test: standard routes are fully accessible alongside monitoring router."""
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "healthy"

    farmers_res = client.get("/api/farmers")
    assert farmers_res.status_code == 200
    assert isinstance(farmers_res.json(), list)

    weather_res = client.get("/api/weather/forecast?location=Thanjavur")
    assert weather_res.status_code == 200
    assert "daily_forecasts" in weather_res.json()

    history_res = client.get("/api/alerts/history")
    assert history_res.status_code == 200
    assert isinstance(history_res.json(), list)


# ---------------------------------------------------------------------------
# 7: Demo SMS remains simulated and never reported as genuinely sent
# ---------------------------------------------------------------------------

def test_demo_sms_remains_simulated_never_reported_sent():
    """In demo mode, all alerts in DB are SIMULATED and alerts_sent is strictly 0."""
    _create_sample_farmer("Kandasamy", "Thanjavur")

    response = client.post("/api/monitoring/run-now")
    assert response.status_code == 200
    summary = response.json()

    # Summary asserts
    assert summary["alerts_simulated"] >= 1
    assert summary["alerts_sent"] == 0

    # DB record asserts
    db = SessionLocal()
    try:
        records = db.query(AlertHistory).all()
        assert len(records) >= 1
        for record in records:
            assert record.status == "SIMULATED"
            assert record.provider == "demo"
    finally:
        db.close()
