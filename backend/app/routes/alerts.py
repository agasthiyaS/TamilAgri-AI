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

@router.post("/send", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def send_farmer_alert(payload: AlertTriggerRequest, db: Session = Depends(get_db)):
    """
    Sends an SMS early warning alert to a registered farmer.
    Prevents duplicate messages within 24 hours unless `force_resend` is true.
    """
    farmer = db.query(Farmer).filter(Farmer.id == payload.farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # 1. Duplicate check (last 24 hours for same hazard and risk level)
    if not payload.force_resend:
        one_day_ago = datetime.now(timezone.utc) - timedelta(hours=24)
        duplicate = db.query(AlertHistory).filter(
            AlertHistory.farmer_id == farmer.id,
            AlertHistory.hazard == payload.hazard,
            AlertHistory.risk_level == payload.risk_level,
            AlertHistory.sent_at >= one_day_ago
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail=f"Duplicate alert suppressed: A {payload.risk_level}-risk alert for '{payload.hazard}' was already sent to {farmer.name} within the last 24 hours. Use 'force_resend=true' to override."
            )

    # 2. Derive warning content
    # If custom_message not provided, compute from risk engine & language service
    message_text = payload.custom_message
    if not message_text:
        # Fetch risk assessment for context
        weather_provider = get_weather_provider()
        forecast = await weather_provider.get_forecast(farmer.location)
        risk_result = evaluate_crop_risk(farmer.location, farmer.crop, farmer.growth_stage, forecast)
        
        # Match hazard details
        matched_hazard = next((h for h in risk_result.hazards if h.hazard.lower() == payload.hazard.lower()), None)
        trigger_val = payload.trigger_value or (matched_hazard.trigger_value if matched_hazard else "Advisory condition")
        
        # Choose language-specific explanation and precaution
        if farmer.preferred_language == "ta":
            reason = matched_hazard.reason_ta if matched_hazard else "பயிர் பாதுகாப்பு முன்னெச்சரிக்கை."
            precaution = matched_hazard.precaution_ta if matched_hazard else "வேளாண் துறை ஆலோசனையைப் பின்பற்றவும்."
        else:
            reason = matched_hazard.reason_en if matched_hazard else "Agricultural risk mitigation required."
            precaution = matched_hazard.precaution_en if matched_hazard else "Follow agricultural department advisories."

        message_text = generate_sms_message(
            language=farmer.preferred_language,
            risk_level=payload.risk_level,
            farmer_name=farmer.name,
            location=farmer.location,
            crop=farmer.crop,
            growth_stage=farmer.growth_stage,
            hazard=payload.hazard,
            trigger_value=trigger_val,
            reason=reason,
            precaution=precaution
        )

    # 3. Dispatch via configured SMS provider
    sms_provider = get_sms_provider()
    dispatch_result = await sms_provider.send_sms(
        to_number=farmer.mobile_number,
        message=message_text
    )

    # 4. Record entry in AlertHistory table
    alert_record = AlertHistory(
        farmer_id=farmer.id,
        farmer_name=farmer.name,
        mobile_number=farmer.mobile_number,
        location=farmer.location,
        crop=farmer.crop,
        growth_stage=farmer.growth_stage,
        hazard=payload.hazard,
        risk_level=payload.risk_level,
        language=farmer.preferred_language,
        message=message_text,
        status=dispatch_result.status,
        provider=dispatch_result.provider,
        provider_message_id=dispatch_result.provider_message_id,
        error_message=dispatch_result.error_message,
        sent_at=datetime.now(timezone.utc)
    )
    db.add(alert_record)
    db.commit()
    db.refresh(alert_record)

    return alert_record

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
        raise HTTPException(status_code=404, detail=f"No registered farmers found matching location '{payload.location}'")

    sent_alerts = []
    sms_provider = get_sms_provider()
    one_day_ago = datetime.now(timezone.utc) - timedelta(hours=24)

    for farmer in target_farmers:
        # Check duplicate
        dup = db.query(AlertHistory).filter(
            AlertHistory.farmer_id == farmer.id,
            AlertHistory.hazard == payload.hazard,
            AlertHistory.risk_level == payload.risk_level,
            AlertHistory.sent_at >= one_day_ago
        ).first()
        if dup:
            continue

        # Generate message
        if farmer.preferred_language == "ta":
            reason = "மாவட்டத்தில் வானிலை இடர்பாடு எதிர்பார்க்கப்படுகிறது."
            precaution = "பாதுகாப்பு வடிகால் மற்றும் முன்னெச்சரிக்கை நடவடிக்கைகளை மேற்கொள்ளவும்."
        else:
            reason = "Adverse weather conditions forecast in district."
            precaution = "Ensure field drainage and take precautionary measures."

        msg = generate_sms_message(
            language=farmer.preferred_language,
            risk_level=payload.risk_level,
            farmer_name=farmer.name,
            location=farmer.location,
            crop=farmer.crop,
            growth_stage=farmer.growth_stage,
            hazard=payload.hazard,
            trigger_value=payload.trigger_value or "Advisory Alert",
            reason=reason,
            precaution=precaution
        )

        res = await sms_provider.send_sms(to_number=farmer.mobile_number, message=msg)

        alert = AlertHistory(
            farmer_id=farmer.id,
            farmer_name=farmer.name,
            mobile_number=farmer.mobile_number,
            location=farmer.location,
            crop=farmer.crop,
            growth_stage=farmer.growth_stage,
            hazard=payload.hazard,
            risk_level=payload.risk_level,
            language=farmer.preferred_language,
            message=msg,
            status=res.status,
            provider=res.provider,
            provider_message_id=res.provider_message_id,
            error_message=res.error_message,
            sent_at=datetime.now(timezone.utc)
        )
        db.add(alert)
        sent_alerts.append(alert)

    db.commit()
    for a in sent_alerts:
        db.refresh(a)

    return sent_alerts

@router.get("/history", response_model=List[AlertResponse])
def get_alert_history(
    hazard: Optional[str] = Query(None, description="Filter by hazard"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    status: Optional[str] = Query(None, description="Filter by status (SIMULATED, DELIVERED, FAILED)"),
    db: Session = Depends(get_db)
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
