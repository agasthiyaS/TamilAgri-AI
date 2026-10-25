from fastapi import APIRouter
from ..schemas.language import WarningGenerationRequest, WarningGenerationResponse
from ..services.language_service import (
    generate_warning_report,
    SUPPORTED_LANGUAGES,
    TAMIL_TERMS,
    DEFAULT_PRECAUTIONS
)

router = APIRouter(prefix="/language", tags=["Language Intelligence"])

@router.post("/warning", response_model=WarningGenerationResponse)
def create_warning_message(payload: WarningGenerationRequest):
    """
    Generates dynamic, farmer-friendly climate warnings in Tamil or English
    based on crop, growth stage, hazard, risk level, and optional measurements/precautions.
    """
    report = generate_warning_report(
        crop=payload.crop,
        growth_stage=payload.growth_stage,
        hazard=payload.hazard,
        risk_level=payload.risk_level,
        language=payload.language,
        trigger_value=payload.trigger_value,
        precaution=payload.precaution,
        farmer_name=payload.farmer_name,
        location=payload.location
    )
    return report

@router.get("/languages")
def get_supported_languages():
    """Lists supported language codes and labels."""
    return [
        {"code": code, "label": label}
        for code, label in SUPPORTED_LANGUAGES.items()
    ]

@router.get("/terms")
def get_terminology_dictionary():
    """Returns official agricultural terminology mappings between English and Tamil."""
    return {
        "tamil_terms": TAMIL_TERMS,
        "default_precautions": DEFAULT_PRECAUTIONS
    }
