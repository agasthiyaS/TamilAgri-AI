from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.farmer import Farmer
from ..models.alert import AlertHistory
from ..schemas.alert import AlertTriggerRequest, BroadcastAlertRequest, AlertResponse
from ..services.language_service import generate_sms_message
from ..services.sms_adapter import get_sms_provider
from ..services.risk_engine import evaluate_crop_risk
from ..services.weather_adapter import get_weather_provider

router = APIRouter(prefix="/alerts", tags=["Early Warnings & SMS"])


# ---------------------------------------------------------------------------
# Reusable alert-dispatch result — carries enough context for both the API
# route (which maps it to HTTP responses) and the future scheduler (which
# logs results without raising HTTPException).
# ---------------------------------------------------------------------------

@dataclass
class AlertDispatchResult:
    """
    Returned by _build_and_dispatch_alert() for every call, regardless of
    outcome.  The API route interprets the fields as HTTP responses; the
    scheduler uses them for logging.
    """
    alert_record: Optional[AlertHistory]  # None when alert was not sent
    was_sent: bool                        # True when SMS was dispatched and recorded
    skip_reason: Optional[str]            # "DUPLICATE" when 24-h guard triggered
    error_message: Optional[str]          # Non-None if an unexpected exception occurred


async def _build_and_dispatch_alert(
    db: Session,
    farmer: Farmer,
    hazard: str,
    risk_level: str,
    trigger_value: Optional[str] = None,
    custom_message: Optional[str] = None,
    force_resend: bool = False,
    reason: Optional[str] = None,
    precaution: Optional[str] = None,
) -> AlertDispatchResult:
    """
    Core alert logic reused by both the API route and the monitoring scheduler.

    Responsibilities:
      1. Duplicate-prevention check (24-h window, keyed on farmer + hazard + risk_level).
      2. Message generation via the Language Intelligence Module.
         - If `custom_message` is supplied it is used as-is.
         - Otherwise the weather forecast and risk engine are consulted to
           derive `trigger_value`, `reason`, and `precaution` in the farmer's
           preferred language, then `generate_sms_message()` builds the text.
         - If `reason`/`precaution` are passed in directly (e.g. by the
           broadcast route or the scheduler) the forecast fetch is skipped.
      3. SMS dispatch via the configured provider (demo by default).
      4. AlertHistory record creation and DB commit.

    Does NOT raise HTTPException — returns an AlertDispatchResult so callers
    can handle outcomes according to their own context (HTTP route vs scheduler).
    """

    # --- 1. Duplicate-prevention check ---
    if not force_resend:
        one_day_ago = datetime.now(timezone.utc) - timedelta(hours=24)
        duplicate = (
            db.query(AlertHistory)
            .filter(
                AlertHistory.farmer_id == farmer.id,
                AlertHistory.hazard == hazard,
                AlertHistory.risk_level == risk_level,
                AlertHistory.sent_at >= one_day_ago,
            )
            .first()
        )
        if duplicate:
            return AlertDispatchResult(
                alert_record=None,
                was_sent=False,
                skip_reason="DUPLICATE",
                error_message=None,
            )

    # --- 2. Derive warning message text ---
    message_text = custom_message

    if not message_text:
        # Use caller-supplied reason/precaution when available (broadcast / scheduler path).
        # Otherwise fetch the forecast and evaluate the risk engine to get accurate details.
        if reason is None or precaution is None:
            weather_provider = get_weather_provider()
            forecast = await weather_provider.get_forecast(farmer.location)
            risk_result = evaluate_crop_risk(
                farmer.location, farmer.crop, farmer.growth_stage, forecast
            )
            matched_hazard = next(
                (h for h in risk_result.hazards if h.hazard.lower() == hazard.lower()),
                None,
            )
            trigger_value = trigger_value or (
                matched_hazard.trigger_value if matched_hazard else "Advisory condition"
            )
            if farmer.preferred_language == "ta":
                reason = (
                    matched_hazard.reason_ta
                    if matched_hazard
                    else "பயிர் பாதுகாப்பு முன்னெச்சரிக்கை."
                )
                precaution = (
                    matched_hazard.precaution_ta
                    if matched_hazard
                    else "வேளாண் துறை ஆலோசனையைப் பின்பற்றவும்."
                )
            else:
                reason = (
                    matched_hazard.reason_en
                    if matched_hazard
                    else "Agricultural risk mitigation required."
                )
                precaution = (
                    matched_hazard.precaution_en
                    if matched_hazard
                    else "Follow agricultural department advisories."
                )

        message_text = generate_sms_message(
            language=farmer.preferred_language,
            risk_level=risk_level,
            farmer_name=farmer.name,
            location=farmer.location,
            crop=farmer.crop,
            growth_stage=farmer.growth_stage,
            hazard=hazard,
            trigger_value=trigger_value or "Advisory condition",
            reason=reason,
            precaution=precaution,
        )

    # --- 3. Dispatch via configured SMS provider ---
    sms_provider = get_sms_provider()
    dispatch_result = await sms_provider.send_sms(
        to_number=farmer.mobile_number,
        message=message_text,
    )

    # --- 4. Persist AlertHistory record ---
    alert_record = AlertHistory(
        farmer_id=farmer.id,
        farmer_name=farmer.name,
        mobile_number=farmer.mobile_number,
        location=farmer.location,
        crop=farmer.crop,
        growth_stage=farmer.growth_stage,
        hazard=hazard,
        risk_level=risk_level,
        language=farmer.preferred_language,
        message=message_text,
        status=dispatch_result.status,
        provider=dispatch_result.provider,
        provider_message_id=dispatch_result.provider_message_id,
        error_message=dispatch_result.error_message,
        sent_at=datetime.now(timezone.utc),
    )
    db.add(alert_record)
    db.commit()
    db.refresh(alert_record)

    return AlertDispatchResult(
        alert_record=alert_record,
        was_sent=True,
        skip_reason=None,
        error_message=dispatch_result.error_message,
    )


# ---------------------------------------------------------------------------
# API Routes — unchanged external behaviour, now delegate to the helper.
# ---------------------------------------------------------------------------

@router.post("/send", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def send_farmer_alert(payload: AlertTriggerRequest, db: Session = Depends(get_db)):
    """
    Sends an SMS early warning alert to a registered farmer.
    Prevents duplicate messages within 24 hours unless `force_resend` is true.
    """
    # Farmer lookup stays in the route — 404 is an HTTP concern, not a scheduler concern.
    farmer = db.query(Farmer).filter(Farmer.id == payload.farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    result = await _build_and_dispatch_alert(
        db=db,
        farmer=farmer,
        hazard=payload.hazard,
        risk_level=payload.risk_level,
        trigger_value=payload.trigger_value,
        custom_message=payload.custom_message,
        force_resend=payload.force_resend,
    )

    # Map the helper result back to the HTTP contract the route has always promised.
    if result.skip_reason == "DUPLICATE":
        raise HTTPException(
            status_code=409,
            detail=(
                f"Duplicate alert suppressed: A {payload.risk_level}-risk alert for "
                f"'{payload.hazard}' was already sent to {farmer.name} within the last "
                f"24 hours. Use 'force_resend=true' to override."
            ),
        )

    return result.alert_record


@router.post("/broadcast", response_model=List[AlertResponse])
async def broadcast_district_alert(payload: BroadcastAlertRequest, db: Session = Depends(get_db)):
    """
    Broadcasts early warnings to all registered farmers in a specific district/location.
    """
    query = db.query(Farmer).filter(Farmer.location.ilike(f"%{payload.location.strip()}%"))
    if payload.crop:
        query = query.filter(Farmer.crop == payload.crop)
    if payload.growth_stage:
        query = query.filter(Farmer.growth_stage == payload.growth_stage)

    target_farmers = query.all()
    if not target_farmers:
        raise HTTPException(
            status_code=404,
            detail=f"No registered farmers found matching location '{payload.location}'",
        )

    sent_alerts = []

    for farmer in target_farmers:
        # Provide language-specific reason/precaution directly so the helper
        # skips the per-farmer forecast fetch (broadcast uses a single advisory).
        if farmer.preferred_language == "ta":
            reason = "மாவட்டத்தில் வானிலை இடர்பாடு எதிர்பார்க்கப்படுகிறது."
            precaution = "பாதுகாப்பு வடிகால் மற்றும் முன்னெச்சரிக்கை நடவடிக்கைகளை மேற்கொள்ளவும்."
        else:
            reason = "Adverse weather conditions forecast in district."
            precaution = "Ensure field drainage and take precautionary measures."

        result = await _build_and_dispatch_alert(
            db=db,
            farmer=farmer,
            hazard=payload.hazard,
            risk_level=payload.risk_level,
            trigger_value=payload.trigger_value or "Advisory Alert",
            force_resend=False,
            reason=reason,
            precaution=precaution,
        )

        # Silently skip duplicates (broadcast contract: continue to next farmer).
        if result.was_sent and result.alert_record:
            sent_alerts.append(result.alert_record)

    return sent_alerts


@router.get("/history", response_model=List[AlertResponse])
def get_alert_history(
    hazard: Optional[str] = Query(None, description="Filter by hazard"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    status: Optional[str] = Query(None, description="Filter by status (SIMULATED, DELIVERED, FAILED)"),
    db: Session = Depends(get_db),
):
    """Retrieves audit trail of all generated warning alerts."""
    query = db.query(AlertHistory)
    if hazard:
        query = query.filter(AlertHistory.hazard == hazard)
    if risk_level:
        query = query.filter(AlertHistory.risk_level == risk_level)
    if status:
        query = query.filter(AlertHistory.status == status)

    return query.order_by(AlertHistory.sent_at.desc()).all()
