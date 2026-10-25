from app.services.language_service import generate_sms_message, translate_term

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
