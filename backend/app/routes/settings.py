from fastapi import APIRouter
from ..config import settings
from ..schemas.farmer import VALID_CROPS, VALID_STAGES
from ..rules.crop_rules import IS_DEMO_RULESET

router = APIRouter(prefix="/settings", tags=["Settings & Metadata"])

@router.get("")
def get_system_settings():
    """Returns application configuration metadata, demo states, and validation lists."""
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE,
        "weather_provider": settings.WEATHER_PROVIDER,
        "sms_provider": settings.SMS_PROVIDER,
        "is_demo_ruleset": IS_DEMO_RULESET,
        "supported_crops": VALID_CROPS,
        "supported_growth_stages": VALID_STAGES,
        "supported_languages": [
            {"code": "ta", "label": "தமிழ் (Tamil)"},
            {"code": "en", "label": "English"}
        ],
        "scientific_disclaimer": (
            "NOTICE: Crop risk evaluation rules are prototype demonstration models. "
            "Verification against Tamil Nadu Agricultural University (TNAU) and IMD Agromet guidelines is in progress. "
            "No liability is assumed for agricultural production decisions based solely on this demo."
        )
    }
