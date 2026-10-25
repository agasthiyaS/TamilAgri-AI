"""
Language Intelligence Module for TamilAgri AI.
Provides structured, farmer-friendly Tamil and English warning narratives,
SMS-friendly formatting, and agricultural terminology translation.
Kept strictly decoupled from climate analysis and weather retrieval logic.
"""

from typing import Dict, Any, Optional

# Supported language codes
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ta": "தமிழ் (Tamil)",
    "en": "English"
}

# Standard agricultural translations for Tamil
TAMIL_TERMS: Dict[str, str] = {
    # Crops
    "Paddy": "நெல்",
    "Rice": "நெல்",
    "paddy": "நெல்",
    
    # Growth Stages
    "Nursery": "நாற்றங்கால் பருவம்",
    "Tillering": "தூர் கட்டும் பருவம்",
    "Flowering": "பூக்கும் பருவம்",
    "Grain filling": "பால் பிடிக்கும் / மணி முதிரும் பருவம்",
    "Harvest": "அறுவடைப் பருவம்",
    
    # Hazards
    "Heavy Rainfall": "கனமழை",
    "Extreme Heat": "கடும் வெப்பம்",
    "Rainfall": "மழைப்பொழிவு",
    "Heat": "வெப்பநிலை",
    
    # Risk Levels
    "High": "அதிக ஆபத்து",
    "Medium": "மிதமான ஆபத்து",
    "Low": "குறைந்த ஆபத்து",
}

# Fallback precautions when verified agronomic advice is not available
DEFAULT_PRECAUTIONS: Dict[str, str] = {
    "en": "Monitor weather updates and follow advice from your local agricultural department.",
    "ta": "வானிலை அறிவிப்புகளைக் கவனித்து, உள்ளூர் வேளாண்மைத் துறையின் ஆலோசனைகளைப் பின்பற்றவும்."
}

# Structured SMS message templates
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

def normalize_language(lang: Optional[str], default: str = "ta") -> str:
    """
    Normalizes a given language input into 'ta' or 'en'.
    Gracefully handles unknown codes, whitespace, mixed case, and None by returning the default.
    """
    if not lang or not isinstance(lang, str):
        return default
    
    cleaned = lang.strip().lower()
    if cleaned in ("ta", "tamil", "ta-in", "தமிழ்"):
        return "ta"
    if cleaned in ("en", "english", "en-us", "en-in"):
        return "en"
    
    return default

def translate_term(term: Optional[str], lang: str = "ta") -> str:
    """
    Translates standard agricultural terms (crops, stages, hazards, risks) to Tamil if requested.
    Returns the original string if term is unknown or English is selected.
    """
    if not term:
        return ""
    
    norm_lang = normalize_language(lang)
    if norm_lang == "ta":
        return TAMIL_TERMS.get(term, term)
    return term

def get_default_precaution(lang: str = "ta") -> str:
    """Returns safe official advisory guidance when a specific verified precaution is unavailable."""
    norm_lang = normalize_language(lang)
    return DEFAULT_PRECAUTIONS.get(norm_lang, DEFAULT_PRECAUTIONS["ta"])

def generate_warning_narrative(
    crop: str = "Paddy",
    growth_stage: str = "Flowering",
    hazard: str = "Heavy Rainfall",
    risk_level: str = "High",
    language: str = "ta",
    trigger_value: Optional[str] = None,
    precaution: Optional[str] = None,
    location: Optional[str] = None
) -> str:
    """
    Generates a natural, farmer-friendly explanatory climate risk warning narrative in Tamil or English.
    Constructs clear sentences suitable for dashboard cards, audio announcements, or advisories.
    """
    lang = normalize_language(language)
    normalized_risk = (risk_level or "Medium").capitalize()
    if normalized_risk not in ("Low", "Medium", "High"):
        normalized_risk = "Medium"

    # Resolve safe precaution
    effective_precaution = precaution.strip() if precaution and precaution.strip() else get_default_precaution(lang)
    trigger_suffix_en = f" ({trigger_value})" if trigger_value and trigger_value.strip() else ""
    trigger_suffix_ta = f" ({trigger_value})" if trigger_value and trigger_value.strip() else ""
    loc_phrase_en = f" in {location.strip()}" if location and location.strip() else ""
    loc_phrase_ta = f"{location.strip()} பகுதியில் " if location and location.strip() else ""

    if lang == "ta":
        crop_ta = translate_term(crop, "ta")
        stage_ta = translate_term(growth_stage, "ta")
        hazard_ta = translate_term(hazard, "ta")
        risk_ta = translate_term(normalized_risk, "ta")

        # Natural Tamil inflections
        crop_genitive = "நெற்பயிரின்" if crop_ta in ("நெல்", "Paddy") else f"{crop_ta}யின்"
        if "பருவம்" in stage_ta:
            stage_locative = stage_ta.replace("பருவம்", "பருவத்தில்")
            stage_dative = stage_ta.replace("பருவம்", "பருவத்திற்கு")
        else:
            stage_locative = f"{stage_ta} பருவத்தில்"
            stage_dative = f"{stage_ta} பருவத்திற்கு"

        if normalized_risk == "High":
            return (
                f"{loc_phrase_ta}{crop_genitive} {stage_locative} {hazard_ta} ஏற்படும் {risk_ta} உள்ளது"
                f"{trigger_suffix_ta}. {effective_precaution}"
            )
        elif normalized_risk == "Medium":
            return (
                f"{loc_phrase_ta}{crop_genitive} {stage_locative} {hazard_ta} தொடர்பான {risk_ta} எதிர்பார்க்கப்படுகிறது"
                f"{trigger_suffix_ta}. {effective_precaution}"
            )
        else: # Low risk
            return (
                f"{loc_phrase_ta}{crop_genitive} {stage_dative} தற்போது வானிலை சாதகமாக உள்ளது. "
                f"{effective_precaution}"
            )
    else:
        crop_en = (crop or "paddy").lower()
        stage_en = (growth_stage or "flowering").lower()
        hazard_en = (hazard or "weather").lower()

        if normalized_risk == "High":
            return (
                f"High {hazard_en} risk is expected during the {stage_en} stage of {crop_en}{loc_phrase_en}"
                f"{trigger_suffix_en}. {effective_precaution}"
            )
        elif normalized_risk == "Medium":
            return (
                f"Moderate {hazard_en} advisory is in effect during the {stage_en} stage of {crop_en}{loc_phrase_en}"
                f"{trigger_suffix_en}. {effective_precaution}"
            )
        else: # Low risk
            return (
                f"Weather conditions are currently favorable for the {stage_en} stage of {crop_en}{loc_phrase_en}. "
                f"{effective_precaution}"
            )

def generate_sms_message(
    language: str,
    risk_level: str,
    farmer_name: Optional[str] = None,
    location: Optional[str] = None,
    crop: str = "Paddy",
    growth_stage: str = "Flowering",
    hazard: str = "Heavy Rainfall",
    trigger_value: Optional[str] = None,
    reason: Optional[str] = None,
    precaution: Optional[str] = None
) -> str:
    """
    Renders a formatted, concise SMS text message in Tamil or English based on preferred language.
    Does NOT invoke external translation APIs; uses verified, clean templates.
    Avoids broken characters, duplicate wording, or empty messages.
    """
    lang = normalize_language(language)
    normalized_risk = (risk_level or "Medium").capitalize()
    if normalized_risk not in ("Low", "Medium", "High"):
        normalized_risk = "Medium"

    templates_for_lang = SMS_TEMPLATES.get(lang, SMS_TEMPLATES["en"])
    template = templates_for_lang.get(normalized_risk, templates_for_lang["Medium"])

    # Fallbacks for optional fields
    display_farmer = farmer_name.strip() if farmer_name and farmer_name.strip() else ("விவசாயி" if lang == "ta" else "Farmer")
    display_loc = location.strip() if location and location.strip() else ("உங்கள் பகுதியில்" if lang == "ta" else "your location")
    display_trigger = trigger_value.strip() if trigger_value and trigger_value.strip() else ("வானிலை எச்சரிக்கை" if lang == "ta" else "Weather Advisory")
    
    # Safe precaution fallback
    effective_precaution = precaution.strip() if precaution and precaution.strip() else get_default_precaution(lang)
    
    # Safe reason fallback
    if reason and reason.strip():
        effective_reason = reason.strip()
    else:
        effective_reason = "பயிர் பாதுகாப்பு முன்னெச்சரிக்கை தேவைப்படுகிறது." if lang == "ta" else "Agricultural risk mitigation recommended."

    # Localize crop, stage, and hazard names if Tamil is selected
    display_crop = translate_term(crop, lang)
    display_stage = translate_term(growth_stage, lang)
    display_hazard = translate_term(hazard, lang)

    formatted = template.format(
        farmer_name=display_farmer,
        location=display_loc,
        crop=display_crop,
        growth_stage=display_stage,
        hazard=display_hazard,
        trigger_value=display_trigger,
        reason=effective_reason,
        precaution=effective_precaution
    )

    # Clean up any extraneous blank lines
    lines = [line.strip() for line in formatted.split("\n") if line.strip()]
    return "\n".join(lines)

def generate_warning_report(
    crop: str = "Paddy",
    growth_stage: str = "Flowering",
    hazard: str = "Heavy Rainfall",
    risk_level: str = "High",
    language: str = "ta",
    trigger_value: Optional[str] = None,
    precaution: Optional[str] = None,
    farmer_name: Optional[str] = None,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    High-level orchestrator returning a complete structured response containing
    localized terms, human-readable narrative, and SMS-formatted text.
    """
    lang = normalize_language(language)
    normalized_risk = (risk_level or "Medium").capitalize()
    if normalized_risk not in ("Low", "Medium", "High"):
        normalized_risk = "Medium"

    effective_precaution = precaution.strip() if precaution and precaution.strip() else get_default_precaution(lang)
    
    narrative = generate_warning_narrative(
        crop=crop,
        growth_stage=growth_stage,
        hazard=hazard,
        risk_level=normalized_risk,
        language=lang,
        trigger_value=trigger_value,
        precaution=effective_precaution,
        location=location
    )

    sms_text = generate_sms_message(
        language=lang,
        risk_level=normalized_risk,
        farmer_name=farmer_name,
        location=location,
        crop=crop,
        growth_stage=growth_stage,
        hazard=hazard,
        trigger_value=trigger_value,
        precaution=effective_precaution
    )

    headline = (
        f"{translate_term(normalized_risk, lang)}: {translate_term(hazard, lang)}"
        if lang == "ta"
        else f"{normalized_risk} Risk: {hazard}"
    )

    return {
        "language": lang,
        "headline": headline,
        "warning_text": narrative,
        "precaution": effective_precaution,
        "sms_text": sms_text,
        "crop_localized": translate_term(crop, lang),
        "stage_localized": translate_term(growth_stage, lang),
        "hazard_localized": translate_term(hazard, lang),
        "risk_level_localized": translate_term(normalized_risk, lang),
    }
