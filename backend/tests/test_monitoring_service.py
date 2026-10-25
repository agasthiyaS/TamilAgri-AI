"""
Stage 2 tests: verify automatic weather risk-monitoring service.

These tests prove:
  - run_monitoring_cycle() iterates over registered farmers.
  - Cycle summary contains all required fields:
      * farmers_checked
      * risks_detected
      * alerts_simulated
      * alerts_sent
      * duplicates_suppressed
      * failures
  - Simulated messages (Demo mode) increment alerts_simulated, while alerts_sent remains 0.
  - Live messages (status == DELIVERED) increment alerts_sent.
  - Farmers with Low risk conditions do not receive alerts (suppressed).
  - Consecutive cycles within 24 hours increment duplicates_suppressed.
  - Farmers sharing the same location share a single weather forecast request.
  - Failed weather requests increment failures and do not crash the cycle.
  - Failed alert dispatches increment failures and do not crash the cycle.
  - Language preferences ('ta' vs 'en') produce appropriate multilingual messages in AlertHistory.
  - is_cycle_running() flag accurately reflects execution state.
"""

from unittest.mock import AsyncMock, patch
import pytest

from app.database import Base, engine, SessionLocal
from app.models.farmer import Farmer
from app.models.alert import AlertHistory
from app.services.monitoring_service import run_monitoring_cycle, is_cycle_running
from app.schemas.weather import WeatherForecastResponse, DailyForecast
from app.services.sms_adapter import SMSDeliveryResult


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


def _create_farmer(name: str, location: str, crop: str = "Paddy", stage: str = "Flowering", lang: str = "ta") -> Farmer:
    db = SessionLocal()
    try:
        farmer = Farmer(
            name=name,
            mobile_number="+919876543210",
            location=location,
            crop=crop,
            growth_stage=stage,
            preferred_language=lang,
        )
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_summary_fields_and_demo_simulation_separation():
    """
    In Demo mode:
      - alerts_simulated must increment.
      - alerts_sent must REMAIN 0.
      - All 6 required fields must be present and correctly populated.
    """
    _create_farmer("Murugan", "Thanjavur", crop="Paddy", stage="Flowering", lang="ta")

    db = SessionLocal()
    try:
        summary = await run_monitoring_cycle(db)

        # 1. Verify all required fields are present
        assert "farmers_checked" in summary
        assert "risks_detected" in summary
        assert "alerts_simulated" in summary
        assert "alerts_sent" in summary
        assert "duplicates_suppressed" in summary
        assert "failures" in summary

        # 2. Verify values
        assert summary["status"] == "completed"
        assert summary["farmers_checked"] == 1
        assert summary["risks_detected"] >= 1
        assert summary["alerts_simulated"] >= 1
        assert summary["alerts_sent"] == 0  # STRICT: In demo mode, alerts_sent must not increase!
        assert summary["duplicates_suppressed"] == 0
        assert summary["failures"] == 0

        # 3. Verify AlertHistory record status
        records = db.query(AlertHistory).filter(AlertHistory.farmer_name == "Murugan").all()
        assert len(records) >= 1
        assert records[0].status == "SIMULATED"
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_live_sms_delivery_increments_alerts_sent():
    """
    When live SMS delivery succeeds (DELIVERED):
      - alerts_sent must increment.
      - alerts_simulated must remain 0.
    """
    _create_farmer("Senthil", "Thanjavur", crop="Paddy", stage="Flowering", lang="en")

    live_result = SMSDeliveryResult(
        success=True,
        status="DELIVERED",
        provider="twilio",
        provider_message_id="SM_TEST_12345",
        error_message=None,
    )

    db = SessionLocal()
    try:
        with patch("app.routes.alerts.get_sms_provider") as mock_get_sms:
            mock_sms = AsyncMock()
            mock_sms.send_sms.return_value = live_result
            mock_get_sms.return_value = mock_sms

            summary = await run_monitoring_cycle(db)
            assert summary["status"] == "completed"
            assert summary["farmers_checked"] == 1
            assert summary["risks_detected"] >= 1
            assert summary["alerts_sent"] >= 1  # Live messages counted under alerts_sent
            assert summary["alerts_simulated"] == 0  # Zero simulated messages
            assert summary["duplicates_suppressed"] == 0
            assert summary["failures"] == 0
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_suppresses_low_risk():
    """When weather has no adverse conditions, risk is Low and no alert is sent or simulated."""
    _create_farmer("Selvam", "SafeZone", crop="Paddy", stage="Nursery", lang="en")

    benign_forecast = WeatherForecastResponse(
        location="SafeZone",
        source="Test Provider",
        period="2026-10-25 to 2026-10-29",
        is_demo=True,
        daily_forecasts=[
            DailyForecast(
                date="2026-10-25",
                temp_max_c=28.0,
                temp_min_c=22.0,
                rainfall_mm=2.0,
                humidity_pct=65.0,
                weather_condition="Clear",
            )
        ],
    )

    db = SessionLocal()
    try:
        with patch("app.services.monitoring_service.get_weather_provider") as mock_get_provider:
            mock_provider = AsyncMock()
            mock_provider.get_forecast.return_value = benign_forecast
            mock_get_provider.return_value = mock_provider

            summary = await run_monitoring_cycle(db)
            assert summary["status"] == "completed"
            assert summary["farmers_checked"] == 1
            assert summary["risks_detected"] == 0  # No High or Medium risk hazards
            assert summary["alerts_simulated"] == 0
            assert summary["alerts_sent"] == 0
            assert summary["duplicates_suppressed"] == 0
            assert summary["failures"] == 0

            # No AlertHistory records should be written
            records = db.query(AlertHistory).all()
            assert len(records) == 0
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_duplicate_prevention_on_consecutive_runs():
    """Running monitoring cycle twice in a row should increment duplicates_suppressed."""
    _create_farmer("Kavitha", "Thanjavur", crop="Paddy", stage="Flowering", lang="ta")

    db = SessionLocal()
    try:
        # First cycle simulates alert
        summary1 = await run_monitoring_cycle(db)
        assert summary1["alerts_simulated"] >= 1
        simulated_first_time = summary1["alerts_simulated"]

        # Second cycle runs immediately: should detect duplicates
        summary2 = await run_monitoring_cycle(db)
        assert summary2["alerts_simulated"] == 0
        assert summary2["alerts_sent"] == 0
        assert summary2["duplicates_suppressed"] == simulated_first_time
        assert summary2["failures"] == 0
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_groups_by_location():
    """Farmers in the same location should only trigger one get_forecast call for that location."""
    _create_farmer("Farmer A", "Thanjavur", crop="Paddy", stage="Flowering")
    _create_farmer("Farmer B", "Thanjavur", crop="Paddy", stage="Tillering")

    db = SessionLocal()
    try:
        with patch("app.services.monitoring_service.get_weather_provider") as mock_get_provider:
            mock_provider = AsyncMock()
            from app.services.weather_adapter import DemoWeatherProvider
            real_demo = DemoWeatherProvider()
            mock_provider.get_forecast.side_effect = real_demo.get_forecast
            mock_get_provider.return_value = mock_provider

            summary = await run_monitoring_cycle(db)
            assert summary["farmers_checked"] == 2
            # Location 'Thanjavur' was fetched exactly once despite 2 farmers
            assert mock_provider.get_forecast.call_count == 1
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_reflects_weather_request_failure_in_failures_count():
    """If one location's weather fetch fails, failures count increments by 1 and other locations proceed."""
    _create_farmer("Farmer Thanjavur", "Thanjavur", crop="Paddy", stage="Flowering")
    _create_farmer("Farmer Madurai", "Madurai", crop="Paddy", stage="Flowering")

    from app.services.weather_adapter import DemoWeatherProvider
    real_demo = DemoWeatherProvider()

    async def mock_get_forecast(location: str):
        if "thanjavur" in location.lower():
            raise ConnectionError("Simulated weather API outage")
        return await real_demo.get_forecast(location)

    db = SessionLocal()
    try:
        with patch("app.services.monitoring_service.get_weather_provider") as mock_get_provider:
            mock_provider = AsyncMock()
            mock_provider.get_forecast.side_effect = mock_get_forecast
            mock_get_provider.return_value = mock_provider

            summary = await run_monitoring_cycle(db)
            assert summary["status"] == "completed"
            # Thanjavur weather failed, Madurai farmer was checked
            assert summary["farmers_checked"] == 1
            assert summary["failures"] == 1  # Exactly 1 failed weather request
            assert summary["alerts_simulated"] >= 1  # Madurai heat alert was simulated
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_reflects_failed_alert_dispatch_in_failures_count():
    """If SMS dispatch fails (status == 'FAILED'), it is counted under failures."""
    _create_farmer("Farmer 1", "Thanjavur", crop="Paddy", stage="Flowering")

    failed_result = SMSDeliveryResult(
        success=False,
        status="FAILED",
        provider="twilio",
        error_message="Gateway connection error",
    )

    db = SessionLocal()
    try:
        with patch("app.routes.alerts.get_sms_provider") as mock_get_sms:
            mock_sms = AsyncMock()
            mock_sms.send_sms.return_value = failed_result
            mock_get_sms.return_value = mock_sms

            summary = await run_monitoring_cycle(db)
            assert summary["status"] == "completed"
            assert summary["farmers_checked"] == 1
            assert summary["failures"] >= 1  # Failed dispatch reflected in failures
            assert summary["alerts_sent"] == 0
            assert summary["alerts_simulated"] == 0
    finally:
        db.close()


@pytest.mark.anyio
async def test_cycle_respects_farmer_preferred_language():
    """Tamil and English farmers receive appropriately localized alerts."""
    _create_farmer("Arun Tamil", "Thanjavur", crop="Paddy", stage="Flowering", lang="ta")
    _create_farmer("John English", "Thanjavur", crop="Paddy", stage="Flowering", lang="en")

    db = SessionLocal()
    try:
        summary = await run_monitoring_cycle(db)
        assert summary["farmers_checked"] == 2
        assert summary["alerts_simulated"] >= 2

        # Check records in AlertHistory
        ta_record = db.query(AlertHistory).filter(AlertHistory.farmer_name == "Arun Tamil").first()
        en_record = db.query(AlertHistory).filter(AlertHistory.farmer_name == "John English").first()

        assert ta_record is not None
        assert ta_record.language == "ta"
        # Check Tamil unicode script is in the message
        assert any("\u0b80" <= char <= "\u0bff" for char in ta_record.message)

        assert en_record is not None
        assert en_record.language == "en"
        assert "TamilAgri Alert" in en_record.message or "Dear" in en_record.message
    finally:
        db.close()


def test_is_cycle_running_default_false():
    """is_cycle_running() must return False when idle."""
    assert is_cycle_running() is False
