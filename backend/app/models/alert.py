from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from ..database import Base

class AlertHistory(Base):
    """
    Log of warnings and SMS dispatch attempts.
    Maintains full audit trail and helps prevent duplicate warnings.
    """
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    farmer_name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False, index=True)
    location = Column(String(100), nullable=False)
    crop = Column(String(50), nullable=False)
    growth_stage = Column(String(50), nullable=False)
    hazard = Column(String(50), nullable=False) # "Heavy Rainfall", "Extreme Heat"
    risk_level = Column(String(20), nullable=False) # "Low", "Medium", "High"
    language = Column(String(10), nullable=False) # "ta" or "en"
    message = Column(Text, nullable=False)
    status = Column(String(30), nullable=False) # "SIMULATED", "DELIVERED", "FAILED", "DUPLICATE_SUPPRESSED"
    provider = Column(String(30), nullable=False) # "demo", "twilio", "generic_webhook"
    provider_message_id = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
