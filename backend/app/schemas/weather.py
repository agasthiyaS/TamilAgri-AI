from typing import List, Optional
from pydantic import BaseModel, Field

class DailyForecast(BaseModel):
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    temp_max_c: float = Field(..., description="Maximum temperature in Celsius")
    temp_min_c: float = Field(..., description="Minimum temperature in Celsius")
    rainfall_mm: float = Field(..., description="Expected daily precipitation in mm")
    humidity_pct: Optional[float] = Field(None, description="Average relative humidity percentage")
    weather_condition: str = Field(..., description="Short weather condition label (e.g. Heavy Rain, Sunny, Hot)")

class WeatherForecastResponse(BaseModel):
    location: str = Field(..., description="Queried location/district")
    source: str = Field(..., description="Weather data source, e.g., Demo Dataset or Open-Meteo")
    period: str = Field(..., description="Forecast window, e.g., 5-Day Outlook")
    is_demo: bool = Field(True, description="Indicates whether this is simulated demo data")
    daily_forecasts: List[DailyForecast] = Field(default_factory=list)
