from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class AlertTriggerRequest(BaseModel):
    farmer_id: int = Field(..., description="ID of registered farmer to alert")
    hazard: str = Field(..., description="Hazard assessed, e.g. Heavy Rainfall or Extreme Heat")
    risk_level: str = Field(..., description="Low, Medium, or High")
    trigger_value: Optional[str] = Field(None, description="Observed trigger condition (e.g. 72mm rain)")
    custom_message: Optional[str] = Field(None, description="Optional manual message override")
    force_resend: bool = Field(False, description="Send even if an alert was sent in the last 24 hours")

class BroadcastAlertRequest(BaseModel):
    location: str = Field(..., description="Target district/location to alert all registered farmers")
    crop: str = Field("Paddy", description="Target crop")
    growth_stage: Optional[str] = Field(None, description="Optional target stage")
    hazard: str = Field(..., description="Hazard type")
    risk_level: str = Field(..., description="High or Medium")
    trigger_value: Optional[str] = Field(None)

class AlertResponse(BaseModel):
    id: int
    farmer_id: Optional[int]
    farmer_name: str
    mobile_number: str
    location: str
    crop: str
    growth_stage: str
    hazard: str
    risk_level: str
    language: str
    message: str
    status: str # "SIMULATED", "DELIVERED", "FAILED", "DUPLICATE_SUPPRESSED"
    provider: str
    provider_message_id: Optional[str]
    error_message: Optional[str]
    sent_at: datetime
    model_config = ConfigDict(from_attributes=True)
