from fastapi import APIRouter, Query, HTTPException
from ..schemas.weather import WeatherForecastResponse
from ..services.weather_adapter import get_weather_provider

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/forecast", response_model=WeatherForecastResponse)
async def get_forecast(
    location: str = Query("Thanjavur", description="Location or Tamil Nadu district name")
):
    """
    Fetches 5-day weather forecast using the configured weather adapter.
    In demo mode, returns realistic Tamil Nadu agricultural conditions.
    """
    if not location or not location.strip():
        raise HTTPException(status_code=400, detail="Location query parameter cannot be empty.")
    provider = get_weather_provider()
    return await provider.get_forecast(location.strip())
