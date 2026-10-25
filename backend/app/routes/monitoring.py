import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.monitoring import MonitoringCycleSummary
from ..services.monitoring_service import (
    run_monitoring_cycle,
    is_cycle_running,
    MonitoringCycleRunningError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["Weather Risk Monitoring"])


@router.post(
    "/run-now",
    response_model=MonitoringCycleSummary,
    status_code=status.HTTP_200_OK,
    summary="Trigger an immediate weather risk-monitoring cycle",
)
async def trigger_manual_monitoring_cycle(db: Session = Depends(get_db)):
    """
    Manually triggers one complete weather risk-monitoring cycle over all registered farmers.

    Returns the cycle summary containing counts of:
      - farmers_checked
      - risks_detected
      - alerts_simulated (demo mode)
      - alerts_sent (live delivered mode)
      - duplicates_suppressed (24h duplicate guard)
      - failures

    Concurrency:
      If a cycle is already running (either via scheduler or another manual request),
      returns HTTP 409 Conflict.

    Configuration:
      Works regardless of whether SCHEDULER_ENABLED is true or false.
    """
    if is_cycle_running():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A monitoring cycle is currently in progress. Please wait for it to complete.",
        )

    try:
        summary = await run_monitoring_cycle(db=db)
        return summary
    except MonitoringCycleRunningError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A monitoring cycle is currently in progress. Please wait for it to complete.",
        )
    except Exception as exc:
        logger.error(f"[Monitoring API] Unexpected error during manual cycle: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while executing the monitoring cycle.",
        )
