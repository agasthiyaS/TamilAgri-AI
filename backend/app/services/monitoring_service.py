"""
Automatic Weather Risk-Monitoring Service.

Periodically reviews weather forecasts for all registered farmers, evaluates
crop-specific risk rules, and automatically triggers multilingual SMS alerts
for 'High' and 'Medium' risk conditions while suppressing duplicates within 24 hours.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from ..config import settings
from ..database import SessionLocal
from ..models.farmer import Farmer
from .risk_engine import evaluate_crop_risk
from .weather_adapter import get_weather_provider

logger = logging.getLogger(__name__)

_cycle_running: bool = False


class MonitoringCycleRunningError(Exception):
    """Raised when an attempt is made to start a monitoring cycle while one is already in progress."""
    pass


def is_cycle_running() -> bool:
    """Returns True if a monitoring cycle is currently actively executing."""
    global _cycle_running
    return _cycle_running


async def run_monitoring_cycle(db: Optional[Session] = None) -> dict:
    """
    Performs one automatic weather risk-monitoring cycle over all registered farmers.

    Workflow:
      1. Concurrency guard: checks if a cycle is already executing.
      2. Query all registered farmers from the database session.
      3. Group farmers by location to avoid duplicate weather forecast fetches.
      4. For each location, fetch the weather forecast once.
      5. For each farmer in that location:
         - Evaluate crop risk based on crop, growth stage, and forecast.
         - Filter for hazards with risk_level in ("High", "Medium"). Low risk is suppressed.
         - For each active hazard, invoke _build_and_dispatch_alert() with language-appropriate
           reason and precaution text.
      6. Aggregate and return execution metrics:
         - farmers_checked
         - risks_detected
         - alerts_simulated (demo mode messages)
         - alerts_sent (live delivered messages; stays 0 in demo mode)
         - duplicates_suppressed (24h duplicate guard)
         - failures (weather request failures, dispatch failures, exceptions)

    Each location and farmer execution is isolated with exception handling so a single
    failure never halts the rest of the cycle.
    """
    global _cycle_running
    if _cycle_running:
        raise MonitoringCycleRunningError("A monitoring cycle is currently in progress.")

    _cycle_running = True
    from ..routes.alerts import _build_and_dispatch_alert

    owns_db = False
    if db is None:
        db = SessionLocal()
        owns_db = True

    start_time = time.time()
    farmers_checked = 0
    risks_detected = 0
    alerts_simulated = 0
    alerts_sent = 0
    duplicates_suppressed = 0
    failures = 0

    try:
        try:
            farmers: List[Farmer] = db.query(Farmer).all()
        except Exception as exc:
            logger.error(f"[Scheduler] Failed to query farmers from database: {exc}", exc_info=True)
            return {
                "status": "failed",
                "error": str(exc),
                "farmers_checked": 0,
                "risks_detected": 0,
                "alerts_simulated": 0,
                "alerts_sent": 0,
                "duplicates_suppressed": 0,
                "duplicates_skipped": 0,
                "failures": 1,
                "cycle_duration_seconds": round(time.time() - start_time, 2),
            }

        # Group farmers by normalized location
        farmers_by_location: Dict[str, List[Farmer]] = {}
        for farmer in farmers:
            loc_key = farmer.location.strip()
            farmers_by_location.setdefault(loc_key, []).append(farmer)

        weather_provider = get_weather_provider()

        for location, loc_farmers in farmers_by_location.items():
            try:
                forecast = await weather_provider.get_forecast(location)
            except Exception as exc:
                logger.error(
                    f"[Scheduler] Failed to fetch weather forecast for location '{location}': {exc}",
                    exc_info=True,
                )
                failures += 1
                continue

            for farmer in loc_farmers:
                farmers_checked += 1
                try:
                    risk_result = evaluate_crop_risk(
                        location=farmer.location,
                        crop=farmer.crop,
                        growth_stage=farmer.growth_stage,
                        forecast=forecast,
                    )

                    # Only hazards with "High" or "Medium" risk level trigger warnings.
                    # Low risk hazards are suppressed.
                    advisory_hazards = [
                        h for h in risk_result.hazards if h.risk_level in ("High", "Medium")
                    ]
                    risks_detected += len(advisory_hazards)

                    for hazard in advisory_hazards:
                        reason = (
                            hazard.reason_ta
                            if farmer.preferred_language == "ta"
                            else hazard.reason_en
                        )
                        precaution = (
                            hazard.precaution_ta
                            if farmer.preferred_language == "ta"
                            else hazard.precaution_en
                        )

                        result = await _build_and_dispatch_alert(
                            db=db,
                            farmer=farmer,
                            hazard=hazard.hazard,
                            risk_level=hazard.risk_level,
                            trigger_value=hazard.trigger_value,
                            reason=reason,
                            precaution=precaution,
                            force_resend=False,
                        )

                        if result.skip_reason == "DUPLICATE":
                            duplicates_suppressed += 1
                        elif result.alert_record:
                            if result.alert_record.status == "SIMULATED":
                                alerts_simulated += 1
                            elif result.alert_record.status == "DELIVERED":
                                alerts_sent += 1
                            elif result.alert_record.status == "FAILED" or result.error_message:
                                failures += 1
                        elif result.error_message:
                            failures += 1

                except Exception as exc:
                    logger.error(
                        f"[Scheduler] Error processing farmer {farmer.id} ({farmer.name}) at '{location}': {exc}",
                        exc_info=True,
                    )
                    failures += 1

        duration = round(time.time() - start_time, 2)
        return {
            "status": "completed",
            "farmers_checked": farmers_checked,
            "risks_detected": risks_detected,
            "alerts_simulated": alerts_simulated,
            "alerts_sent": alerts_sent,
            "duplicates_suppressed": duplicates_suppressed,
            "duplicates_skipped": duplicates_suppressed,
            "failures": failures,
            "cycle_duration_seconds": duration,
        }

    finally:
        _cycle_running = False
        if owns_db and db:
            db.close()


async def monitoring_loop(initial_delay_seconds: Optional[int] = None):
    """
    Continuous background loop that runs run_monitoring_cycle() periodically.
    Designed to be launched as an asyncio.Task inside the FastAPI lifespan.
    Handles graceful cancellation (CancelledError) during application shutdown.
    """
    interval_seconds = getattr(settings, "SCHEDULER_INTERVAL_MINUTES", 60) * 60
    delay = (
        initial_delay_seconds
        if initial_delay_seconds is not None
        else interval_seconds
    )

    logger.info(
        f"[Scheduler] Monitoring loop started. Initial delay: {delay}s, interval: {interval_seconds}s"
    )

    try:
        if delay > 0:
            await asyncio.sleep(delay)

        while True:
            if is_cycle_running():
                logger.warning(
                    "[Scheduler] Previous monitoring cycle still executing. Skipping this interval tick."
                )
            else:
                try:
                    summary = await run_monitoring_cycle()
                    logger.info(f"[Scheduler] Periodic monitoring cycle completed: {summary}")
                except MonitoringCycleRunningError:
                    logger.warning("[Scheduler] Monitoring cycle skipped due to active cycle.")
                except Exception as exc:
                    logger.error(
                        f"[Scheduler] Unhandled error during scheduled monitoring cycle: {exc}",
                        exc_info=True,
                    )

            await asyncio.sleep(interval_seconds)

    except asyncio.CancelledError:
        logger.info("[Scheduler] Monitoring loop task received cancellation. Exiting cleanly.")
        raise
