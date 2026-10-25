import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.language_service import (
    generate_sms_message,
    generate_warning_narrative,
    generate_warning_report,
    normalize_language,
    get_default_precaution,
    translate_term,
    SUPPORTED_LANGUAGES,
    TAMIL_TERMS
)

client = TestClient(app)

# 1. Existing baseline tests (preserved)
def test_tamil_sms_template():
    msg = generate_sms_message(
        language="ta",
        risk_level="High",
        farmer_name="செல்வக்குமார்",
        location="Thanjavur",
        crop="Paddy",
        growth_stage="Flowering",
        hazard="Heavy Rainfall",
        trigger_value="68.5 mm",
        reason="மகரந்த தூள்கள் அடித்துச் செல்லப்படும்.",
        precaution="உபரி நீரை உடனே வடிக்கவும்."
    )

    assert "தமிழ் அக்ரி AI எச்சரிக்கை: அதிக ஆபத்து" in msg
    assert "செல்வக்குமார்" in msg
    assert "நெல்" in msg
    assert "பூக்கும் பருவம்" in msg
    assert "கனமழை" in msg
    assert "உபரி நீரை உடனே வடிக்கவும்" in msg

def test_english_sms_template():
    msg = generate_sms_message(
        language="en",
        risk_level="Medium",
        farmer_name="Murugan",
        location="Madurai",
        crop="Paddy",
        growth_stage="Tillering",
        hazard="Extreme Heat",
        trigger_value="40.8 °C",
        reason="Warm temperature increases water loss.",
        precaution="Keep 5cm water level to buffer heat."
    )

    assert "TamilAgri AI Advisory: Medium Risk" in msg
    assert "Murugan" in msg
    assert "Paddy" in msg
    assert "Tillering" in msg
    assert "Extreme Heat" in msg
    assert "Keep 5cm water level" in msg

def test_terminology_translation():
    assert translate_term("Paddy", "ta") == "நெல்"
    assert translate_term("Harvest", "ta") == "அறுவடைப் பருவம்"
    assert translate_term("Paddy", "en") == "Paddy"
    assert translate_term(None, "ta") == ""
    assert translate_term("UnknownTerm", "ta") == "UnknownTerm"

# 2. English Warning Narrative Generation
def test_english_warning_narrative_high_risk():
    narrative = generate_warning_narrative(
        crop="Paddy",
        growth_stage="Flowering",
        hazard="Heavy Rainfall",
        risk_level="High",
        language="en",
        trigger_value="Rainfall: 68.5 mm",
        location="Thanjavur"
    )

    assert "High heavy rainfall risk is expected during the flowering stage of paddy in Thanjavur" in narrative
    assert "(Rainfall: 68.5 mm)" in narrative
    # When precaution is omitted, safe default must be included
    assert "agricultural department" in narrative

# 3. Tamil Warning Narrative Generation
def test_tamil_warning_narrative_high_risk():
    narrative = generate_warning_narrative(
        crop="Paddy",
        growth_stage="Flowering",
        hazard="Heavy Rainfall",
        risk_level="High",
        language="ta",
        trigger_value="மழை: 68.5 mm",
        location="தஞ்சாவூர்"
    )

    assert "தஞ்சாவூர் பகுதியில் நெற்பயிரின் பூக்கும் பருவத்தில் கனமழை ஏற்படும் அதிக ஆபத்து உள்ளது" in narrative
    assert "(மழை: 68.5 mm)" in narrative
    assert "வேளாண்மைத் துறையின் ஆலோசனைகளைப் பின்பற்றவும்" in narrative

# 4. Different Risk Levels (Medium and Low)
def test_warning_narrative_medium_and_low_risk():
    # Medium risk English
    med_en = generate_warning_narrative(
        crop="Paddy",
        growth_stage="Tillering",
        hazard="Extreme Heat",
        risk_level="Medium",
        language="en",
        trigger_value="40.0 °C",
        precaution="Maintain 5cm shallow water layer."
    )
    assert "Moderate extreme heat advisory is in effect" in med_en
    assert "Maintain 5cm shallow water layer." in med_en

    # Low risk Tamil
    low_ta = generate_warning_narrative(
        crop="Paddy",
        growth_stage="Nursery",
        hazard="Heavy Rainfall",
        risk_level="Low",
        language="ta"
    )
    assert "வானிலை சாதகமாக உள்ளது" in low_ta
    assert "ஆலோசனைகளைப் பின்பற்றவும்" in low_ta

# 5. Language Normalization and Graceful Fallback
def test_language_normalization_and_fallback():
    assert normalize_language("ta") == "ta"
    assert normalize_language("tamil") == "ta"
    assert normalize_language("TA-IN") == "ta"
    assert normalize_language("en") == "en"
    assert normalize_language("ENGLISH") == "en"
    # Invalid codes fallback to default 'ta'
    assert normalize_language("fr") == "ta"
    assert normalize_language("es") == "ta"
    assert normalize_language("") == "ta"
    assert normalize_language(None) == "ta"
    assert normalize_language(None, default="en") == "en"

# 6. Fallback When Verified Precautions Are Unavailable
def test_missing_precaution_fallback():
    precaution_en = get_default_precaution("en")
    precaution_ta = get_default_precaution("ta")

    assert "agricultural department" in precaution_en
    assert "வேளாண்மைத் துறை" in precaution_ta

    # Test in narrative when precaution is None or whitespace
    narrative_empty_prec = generate_warning_narrative(
        crop="Paddy",
        growth_stage="Harvest",
        hazard="Heavy Rainfall",
        risk_level="High",
        language="en",
        precaution="   "
    )
    assert "agricultural department" in narrative_empty_prec

# 7. SMS Formatting and Cleanliness
def test_sms_formatting_cleanliness():
    sms = generate_sms_message(
        language="en",
        risk_level="High",
        farmer_name=None, # Missing farmer name
        location=None,    # Missing location
        crop="Paddy",
        growth_stage="Harvest",
        hazard="Heavy Rainfall",
        trigger_value=None, # Missing trigger value
        reason=None,        # Missing reason
        precaution=None     # Missing precaution
    )

    # Must contain fallback tokens gracefully without crashing
    assert "Farmer" in sms
    assert "your location" in sms
    assert "Paddy" in sms
    assert "Harvest" in sms
    assert "Weather Advisory" in sms
    assert "TamilAgri Advisory" in sms
    # No blank lines clumped together
    assert "\n\n\n" not in sms

# 8. Tamil Unicode Preservation
def test_tamil_unicode_preservation():
    tamil_sample = "தமிழ் அக்ரி AI எச்சரிக்கை: நெற்பயிர் நாற்றங்கால் பருவம்"
    encoded = tamil_sample.encode("utf-8")
    decoded = encoded.decode("utf-8")
    assert decoded == tamil_sample

    msg = generate_sms_message(
        language="ta",
        risk_level="High",
        farmer_name="அகத்தியன்",
        location="மதுரை",
        crop="Paddy",
        growth_stage="Tillering",
        hazard="Extreme Heat",
        trigger_value="41°C",
        reason="வெப்ப அலை தாக்கம்",
        precaution="மாலையில் நீர் பாய்ச்சவும்"
    )
    assert "அகத்தியன்" in msg
    assert "மதுரை" in msg
    assert "தூர் கட்டும் பருவம்" in msg
    assert "கடும் வெப்பம்" in msg

# 9. Complete Warning Report Orchestration
def test_generate_warning_report():
    report = generate_warning_report(
        crop="Paddy",
        growth_stage="Flowering",
        hazard="Heavy Rainfall",
        risk_level="High",
        language="ta",
        trigger_value="70 mm",
        farmer_name="கார்த்திக்",
        location="தஞ்சாவூர்"
    )

    assert report["language"] == "ta"
    assert "அதிக ஆபத்து: கனமழை" in report["headline"]
    assert "பூக்கும் பருவம்" in report["stage_localized"]
    assert "கனமழை" in report["hazard_localized"]
    assert "warning_text" in report
    assert "sms_text" in report
    assert "கார்த்திக்" in report["sms_text"]

# 10. API Integration Endpoints
def test_api_language_endpoints():
    # POST /api/language/warning
    payload = {
        "crop": "Paddy",
        "growth_stage": "Flowering",
        "hazard": "Heavy Rainfall",
        "risk_level": "High",
        "language": "en",
        "trigger_value": "65mm",
        "location": "Thanjavur"
    }
    res = client.post("/api/language/warning", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "risk is expected during the flowering stage of paddy" in data["warning_text"]
    assert data["crop_localized"] == "Paddy"

    # GET /api/language/languages
    lang_res = client.get("/api/language/languages")
    assert lang_res.status_code == 200
    languages = lang_res.json()
    assert any(item["code"] == "ta" for item in languages)
    assert any(item["code"] == "en" for item in languages)

    # GET /api/language/terms
    terms_res = client.get("/api/language/terms")
    assert terms_res.status_code == 200
    terms_data = terms_res.json()
    assert "tamil_terms" in terms_data
    assert terms_data["tamil_terms"]["Paddy"] == "நெல்"
