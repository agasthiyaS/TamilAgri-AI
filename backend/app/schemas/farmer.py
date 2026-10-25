import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

VALID_CROPS = ["Paddy"]
VALID_STAGES = ["Nursery", "Tillering", "Flowering", "Grain filling", "Harvest"]
VALID_LANGUAGES = ["ta", "en"]

class FarmerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Farmer full name")
    mobile_number: str = Field(..., description="Indian 10-digit mobile number, optionally with +91")
    location: str = Field(..., min_length=2, max_length=100, description="District / Village name in Tamil Nadu")
    crop: str = Field(default="Paddy", description="Cultivated crop")
    growth_stage: str = Field(default="Nursery", description="Current stage of crop growth")
    preferred_language: str = Field(default="ta", description="'ta' for Tamil or 'en' for English")

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        # Check standard 10-digit or +91XXXXXXXXXX
        if re.match(r"^(\+91)?[6-9]\d{9}$", cleaned):
            # Normalize to 10 digits without prefix for local consistency, or keep standard format
            if cleaned.startswith("+91"):
                return cleaned
            return f"+91{cleaned}"
        raise ValueError("Invalid mobile number. Please provide a valid 10-digit Indian phone number (e.g., 9876543210).")

    @field_validator("crop")
    @classmethod
    def validate_crop(cls, v: str) -> str:
        if v not in VALID_CROPS:
            raise ValueError(f"Crop must be one of: {', '.join(VALID_CROPS)}")
        return v

    @field_validator("growth_stage")
    @classmethod
    def validate_growth_stage(cls, v: str) -> str:
        if v not in VALID_STAGES:
            raise ValueError(f"Growth stage must be one of: {', '.join(VALID_STAGES)}")
        return v

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v.lower() not in VALID_LANGUAGES:
            raise ValueError("Preferred language must be 'ta' (Tamil) or 'en' (English)")
        return v.lower()

class FarmerCreate(FarmerBase):
    pass

class FarmerResponse(FarmerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
