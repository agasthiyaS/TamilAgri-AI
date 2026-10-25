from fastapi import APIRouter
from ..schemas.risk import RiskAnalysisRequest, RiskAnalysisResult
from ..services.weather_adapter import get_weather_provider
from ..services.risk_engine import evaluate_crop_risk

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])

@router.post("/analyze", response_model=RiskAnalysisResult)
async def analyze_crop_risk(payload: RiskAnalysisRequest):
    """
    Evaluates agricultural climate risks for a given location, crop, and growth stage.
    If forecast data is omitted, it automatically fetches forecast via the weather provider adapter.
    """
    forecast = payload.forecast_data
    if not forecast:
        provider = get_weather_provider()
        forecast = await provider.get_forecast(payload.location)

    result = evaluate_crop_risk(
        location=payload.location,
        crop=payload.crop,
        growth_stage=payload.growth_stage,
        forecast=forecast
    )
    return result
