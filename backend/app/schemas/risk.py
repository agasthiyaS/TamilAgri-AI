from typing import List, Optional
from pydantic import BaseModel, Field
from .weather import WeatherForecastResponse

class RiskAnalysisRequest(BaseModel):
    location: str = Field(..., description="Location/District name")
    crop: str = Field("Paddy", description="Crop name (e.g. Paddy)")
    growth_stage: str = Field(..., description="Growth stage: Nursery, Tillering, Flowering, Grain filling, or Harvest")
    forecast_data: Optional[WeatherForecastResponse] = Field(None, description="Optional pre-fetched forecast")

class HazardAssessment(BaseModel):
    hazard: str = Field(..., description="Hazard type, e.g. Heavy Rainfall or Extreme Heat")
    risk_level: str = Field(..., description="Low, Medium, or High")
    trigger_value: str = Field(..., description="Observed trigger condition (e.g., Rainfall: 68mm / Temp: 41°C)")
    threshold_info: str = Field(..., description="Threshold evaluated from rules")
    reason_en: str = Field(..., description="Explanation in simple English")
    reason_ta: str = Field(..., description="Explanation in simple Tamil")
    precaution_en: str = Field(..., description="Recommended agricultural precaution in English")
    precaution_ta: str = Field(..., description="Recommended agricultural precaution in Tamil")
    is_demo_rule: bool = Field(True, description="Always marked True for DEMO rules pending TNAU verification")

class RiskAnalysisResult(BaseModel):
    location: str
    crop: str
    growth_stage: str
    overall_risk: str # "Low", "Medium", "High"
    forecast_source: str
    forecast_period: str
    is_demo: bool
    hazards: List[HazardAssessment]
    scientific_disclaimer: str = Field(
        "DEMO ADVISORY: Thresholds are for hackathon demonstration. "
        "Consult official Tamil Nadu Agricultural University (TNAU) advisories before taking field action."
    )
