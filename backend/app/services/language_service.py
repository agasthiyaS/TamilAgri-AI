"""
Language Intelligence Module for TamilAgri AI.
Contains structured Tamil and English templates for alerts, warnings, and UI content.
Kept strictly decoupled from climate analysis logic.
"""

from typing import Dict, Any

SMS_TEMPLATES: Dict[str, Dict[str, str]] = {
    "en": {
        "High": (
            "[TamilAgri AI ALERT: HIGH RISK]\n"
            "Dear {farmer_name}, for your {crop} ({growth_stage}) in {location}:\n"
            "WARNING: {hazard} alert ({trigger_value}).\n"
            "Reason: {reason}\n"
            "Precaution: {precaution}\n"
            "- TamilAgri Advisory (Demo Mode)"
        ),
        "Medium": (
            "[TamilAgri AI Advisory: Medium Risk]\n"
            "Dear {farmer_name}, {location} - {crop} ({growth_stage}):\n"
            "Notice: {hazard} ({trigger_value}).\n"
            "Precaution: {precaution}\n"
            "- TamilAgri Advisory"
        ),
        "Low": (
            "[TamilAgri AI Update]\n"
            "Dear {farmer_name}, weather in {location} is favorable for {crop} ({growth_stage}).\n"
            "Precaution: {precaution}\n"
            "- TamilAgri"
        ),
    },
    "ta": {
        "High": (
            "[தமிழ் அக்ரி AI எச்சரிக்கை: அதிக ஆபத்து]\n"
            "வணக்கம் {farmer_name}, {location} பகுதியில் உள்ள உங்கள் {crop} ({growth_stage}) பயிருக்கு:\n"
            "எச்சரிக்கை: {hazard} அபாயம் ({trigger_value}).\n"
            "காரணம்: {reason}\n"
            "பரிந்துரை: {precaution}\n"
            "- தமிழ்நாடு வேளாண் எச்சரிக்கை (மாதிரி முறை)"
        ),
        "Medium": (
            "[தமிழ் அக்ரி AI ஆலோசனை: மிதமான ஆபத்து]\n"
            "வணக்கம் {farmer_name}, {location} - {crop} ({growth_stage}):\n"
            "தகவல்: {hazard} ({trigger_value}).\n"
            "பரிந்துரை: {precaution}\n"
            "- தமிழ் அக்ரி"
        ),
        "Low": (
            "[தமிழ் அக்ரி AI தகவல்]\n"
            "வணக்கம் {farmer_name}, {location} பகுதியில் {crop} ({growth_stage}) பயிருக்கு வானிலை சாதகமாக உள்ளது.\n"
            "பரிந்துரை: {precaution}\n"
            "- தமிழ் அக்ரி"
        ),
    }
}

# Tamil terminology mappings for agricultural terms
TAMIL_TERMS: Dict[str, str] = {
    "Paddy": "நெல்",
    "Nursery": "நாற்றங்கால் பருவம்",
    "Tillering": "தூர் கட்டும் பருவம்",
    "Flowering": "பூக்கும் பருவம்",
    "Grain filling": "பால் பிடிக்கும் / மணி முதிரும் பருவம்",
    "Harvest": "அறுவடைப் பருவம்",
    "Heavy Rainfall": "கனமழை",
    "Extreme Heat": "கடும் வெப்பம்",
    "Low": "குறைந்த ஆபத்து",
    "Medium": "மிதமான ஆபத்து",
    "High": "அதிக ஆபத்து",
}

def translate_term(term: str, lang: str = "ta") -> str:
    """Translates standard agricultural labels to Tamil if requested."""
    if lang == "ta":
        return TAMIL_TERMS.get(term, term)
    return term

def generate_sms_message(
    language: str,
    risk_level: str,
    farmer_name: str,
    location: str,
    crop: str,
    growth_stage: str,
    hazard: str,
    trigger_value: str,
    reason: str,
    precaution: str
) -> str:
    """
    Renders a formatted SMS text message in Tamil or English based on farmer's preferred language.
    Does NOT invoke fake AI translation APIs; uses verified templates.
    """
    lang = "ta" if language.lower() in ("ta", "tamil") else "en"
    templates_for_lang = SMS_TEMPLATES.get(lang, SMS_TEMPLATES["en"])
    template = templates_for_lang.get(risk_level, templates_for_lang["Medium"])

    # Localize crop, stage, and hazard names if Tamil is selected
    display_crop = translate_term(crop, lang)
    display_stage = translate_term(growth_stage, lang)
    display_hazard = translate_term(hazard, lang)

    return template.format(
        farmer_name=farmer_name,
        location=location,
        crop=display_crop,
        growth_stage=display_stage,
        hazard=display_hazard,
        trigger_value=trigger_value,
        reason=reason,
        precaution=precaution
    )
