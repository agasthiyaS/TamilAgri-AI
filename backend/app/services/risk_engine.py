from typing import List
from ..schemas.weather import WeatherForecastResponse
from ..schemas.risk import HazardAssessment, RiskAnalysisResult
from ..rules.crop_rules import PADDY_RISK_RULES, IS_DEMO_RULESET

RISK_ORDER = {"Low": 1, "Medium": 2, "High": 3}

def evaluate_crop_risk(
    location: str,
    crop: str,
    growth_stage: str,
    forecast: WeatherForecastResponse
) -> RiskAnalysisResult:
    """
    Evaluates agricultural risks for a given crop and stage based on forecast data.
    Separated strictly from API network retrieval.
    """
    # Currently Paddy is the supported crop
    crop_name = "Paddy" if crop.strip().lower() == "paddy" else crop.strip()
    stage_rules = PADDY_RISK_RULES.get(growth_stage)

    # Fallback to Nursery if stage not found
    if not stage_rules:
        stage_rules = PADDY_RISK_RULES["Nursery"]
        growth_stage = "Nursery"

    # Analyze max rain and max temperature across the forecast window
    daily_list = forecast.daily_forecasts
    max_rain = max([d.rainfall_mm for d in daily_list]) if daily_list else 0.0
    max_temp = max([d.temp_max_c for d in daily_list]) if daily_list else 30.0

    hazards_evaluated: List[HazardAssessment] = []

    # 1. Evaluate Heavy Rainfall Hazard
    rain_rules = stage_rules.get("Heavy Rainfall", {})
    rain_high = rain_rules.get("high", {})
    rain_med = rain_rules.get("medium", {})
    rain_low = rain_rules.get("low", {})

    if max_rain >= rain_high.get("threshold_rainfall_mm", 999.0):
        rain_level = "High"
        r_en = rain_high.get("reason_en", "")
        r_ta = rain_high.get("reason_ta", "")
        p_en = rain_high.get("precaution_en", "")
        p_ta = rain_high.get("precaution_ta", "")
        th_info = f"Rain >= {rain_high.get('threshold_rainfall_mm')}mm"
    elif max_rain >= rain_med.get("threshold_rainfall_mm", 999.0):
        rain_level = "Medium"
        r_en = rain_med.get("reason_en", "")
        r_ta = rain_med.get("reason_ta", "")
        p_en = rain_med.get("precaution_en", "")
        p_ta = rain_med.get("precaution_ta", "")
        th_info = f"Rain >= {rain_med.get('threshold_rainfall_mm')}mm"
    else:
        rain_level = "Low"
        r_en = rain_low.get("reason_en", "Rainfall within safe limits.")
        r_ta = rain_low.get("reason_ta", "மழைப்பொழிவு பாதுகாப்பான வரம்பிற்குள் உள்ளது.")
        p_en = rain_low.get("precaution_en", "Standard water management.")
        p_ta = rain_low.get("precaution_ta", "வழக்கமான நீர்ப்பாசன முறையைத் தொடரவும்.")
        th_info = f"Rain < {rain_med.get('threshold_rainfall_mm', 25.0)}mm"

    hazards_evaluated.append(
        HazardAssessment(
            hazard="Heavy Rainfall",
            risk_level=rain_level,
            trigger_value=f"Peak: {max_rain:.1f} mm/day",
            threshold_info=th_info,
            reason_en=r_en,
            reason_ta=r_ta,
            precaution_en=p_en,
            precaution_ta=p_ta,
            is_demo_rule=IS_DEMO_RULESET
        )
    )

    # 2. Evaluate Extreme Heat Hazard
    heat_rules = stage_rules.get("Extreme Heat", {})
    heat_high = heat_rules.get("high", {})
    heat_med = heat_rules.get("medium", {})
    heat_low = heat_rules.get("low", {})

    if max_temp >= heat_high.get("threshold_temp_c", 999.0):
        heat_level = "High"
        h_r_en = heat_high.get("reason_en", "")
        h_r_ta = heat_high.get("reason_ta", "")
        h_p_en = heat_high.get("precaution_en", "")
        h_p_ta = heat_high.get("precaution_ta", "")
        h_th_info = f"Max Temp >= {heat_high.get('threshold_temp_c')}°C"
    elif max_temp >= heat_med.get("threshold_temp_c", 999.0):
        heat_level = "Medium"
        h_r_en = heat_med.get("reason_en", "")
        h_r_ta = heat_med.get("reason_ta", "")
        h_p_en = heat_med.get("precaution_en", "")
        h_p_ta = heat_med.get("precaution_ta", "")
        h_th_info = f"Max Temp >= {heat_med.get('threshold_temp_c')}°C"
    else:
        heat_level = "Low"
        h_r_en = heat_low.get("reason_en", "Daytime temperature within optimal limits.")
        h_r_ta = heat_low.get("reason_ta", "வெப்பநிலை உகந்த அளவில் உள்ளது.")
        h_p_en = heat_low.get("precaution_en", "Continue regular operations.")
        h_p_ta = heat_low.get("precaution_ta", "வழக்கமான வேளாண் பணிகளைத் தொடரலாம்.")
        h_th_info = f"Max Temp < {heat_med.get('threshold_temp_c', 35.0)}°C"

    hazards_evaluated.append(
        HazardAssessment(
            hazard="Extreme Heat",
            risk_level=heat_level,
            trigger_value=f"Peak: {max_temp:.1f} °C",
            threshold_info=h_th_info,
            reason_en=h_r_en,
            reason_ta=h_r_ta,
            precaution_en=h_p_en,
            precaution_ta=h_p_ta,
            is_demo_rule=IS_DEMO_RULESET
        )
    )

    # Determine overall risk
    overall_level = "Low"
    for h in hazards_evaluated:
        if RISK_ORDER[h.risk_level] > RISK_ORDER[overall_level]:
            overall_level = h.risk_level

    return RiskAnalysisResult(
        location=location,
        crop=crop_name,
        growth_stage=growth_stage,
        overall_risk=overall_level,
        forecast_source=forecast.source,
        forecast_period=forecast.period,
        is_demo=forecast.is_demo or IS_DEMO_RULESET,
        hazards=hazards_evaluated
    )
