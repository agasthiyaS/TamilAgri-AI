from typing import Optional
from pydantic import BaseModel, Field

class WarningGenerationRequest(BaseModel):
    crop: str = Field(default="Paddy", description="Crop name (e.g. Paddy)")
    growth_stage: str = Field(default="Flowering", description="Crop growth stage: Nursery, Tillering, Flowering, Grain filling, or Harvest")
    hazard: str = Field(default="Heavy Rainfall", description="Weather hazard, e.g. Heavy Rainfall or Extreme Heat")
    risk_level: str = Field(default="High", description="Assessed risk level: Low, Medium, or High")
    language: str = Field(default="ta", description="Preferred language code ('ta' for Tamil, 'en' for English)")
    trigger_value: Optional[str] = Field(None, description="Observed weather trigger value, e.g. 68.5 mm or 40.8 °C")
    precaution: Optional[str] = Field(None, description="Verified or custom agricultural precaution")
    farmer_name: Optional[str] = Field(None, description="Optional recipient farmer name")
    location: Optional[str] = Field(None, description="Optional village / district name")

class WarningGenerationResponse(BaseModel):
    language: str
    headline: str
    warning_text: str
    precaution: str
    sms_text: str
    crop_localized: str
    stage_localized: str
    hazard_localized: str
    risk_level_localized: str
