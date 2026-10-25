from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any
import httpx
from fastapi import HTTPException
from ..config import settings
from ..schemas.weather import WeatherForecastResponse, DailyForecast

# Predefined coordinates for common Tamil Nadu agricultural districts
TAMIL_NADU_DISTRICTS: Dict[str, Dict[str, Any]] = {
    "thanjavur": {"lat": 10.7870, "lon": 79.1378, "name": "Thanjavur (Delta Hub)"},
    "thiruvarur": {"lat": 10.7725, "lon": 79.6366, "name": "Thiruvarur"},
    "nagapattinam": {"lat": 10.7672, "lon": 79.8449, "name": "Nagapattinam"},
    "tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "name": "Tiruchirappalli"},
    "madurai": {"lat": 9.9252, "lon": 78.1198, "name": "Madurai"},
    "coimbatore": {"lat": 11.0168, "lon": 76.9558, "name": "Coimbatore"},
    "cuddalore": {"lat": 11.7480, "lon": 79.7714, "name": "Cuddalore"},
    "salem": {"lat": 11.6643, "lon": 78.1460, "name": "Salem"},
    "tirunelveli": {"lat": 8.7139, "lon": 77.7567, "name": "Tirunelveli"},
    "villupuram": {"lat": 11.9401, "lon": 79.4861, "name": "Villupuram"},
}

class BaseWeatherProvider(ABC):
    @abstractmethod
    async def get_forecast(self, location: str) -> WeatherForecastResponse:
        pass

class DemoWeatherProvider(BaseWeatherProvider):
    """
    Simulated Weather Provider supplying realistic Tamil Nadu district forecasts.
    Does NOT require internet access or external credentials.
    """
    async def get_forecast(self, location: str) -> WeatherForecastResponse:
        loc_key = location.strip().lower()
        today = datetime.now()
        
        # Scenarios tailored to demonstrate both Heavy Rain and Extreme Heat alerts
        if "thanjavur" in loc_key or "delta" in loc_key or "thiruvarur" in loc_key:
            # Heavy Rain scenario for Cauvery Delta
            forecasts = [
                DailyForecast(
                    date=(today + timedelta(days=0)).strftime("%Y-%m-%d"),
                    temp_max_c=31.5,
                    temp_min_c=24.0,
                    rainfall_mm=22.0,
                    humidity_pct=88.0,
                    weather_condition="Scattered Showers"
                ),
                DailyForecast(
                    date=(today + timedelta(days=1)).strftime("%Y-%m-%d"),
                    temp_max_c=29.0,
                    temp_min_c=23.5,
                    rainfall_mm=68.5, # Heavy rain trigger (>50mm)
                    humidity_pct=94.0,
                    weather_condition="Heavy Monsoon Downpour"
                ),
                DailyForecast(
                    date=(today + timedelta(days=2)).strftime("%Y-%m-%d"),
                    temp_max_c=28.5,
                    temp_min_c=23.0,
                    rainfall_mm=45.0,
                    humidity_pct=92.0,
                    weather_condition="Continuous Rain"
                ),
                DailyForecast(
                    date=(today + timedelta(days=3)).strftime("%Y-%m-%d"),
                    temp_max_c=32.0,
                    temp_min_c=24.5,
                    rainfall_mm=12.0,
                    humidity_pct=80.0,
                    weather_condition="Light Drizzle"
                ),
                DailyForecast(
                    date=(today + timedelta(days=4)).strftime("%Y-%m-%d"),
                    temp_max_c=33.5,
                    temp_min_c=25.0,
                    rainfall_mm=3.0,
                    humidity_pct=75.0,
                    weather_condition="Partly Cloudy"
                ),
            ]
        elif "madurai" in loc_key or "salem" in loc_key or "heat" in loc_key:
            # Extreme Heat scenario for Southern/Interior TN
            forecasts = [
                DailyForecast(
                    date=(today + timedelta(days=0)).strftime("%Y-%m-%d"),
                    temp_max_c=38.2,
                    temp_min_c=27.5,
                    rainfall_mm=0.0,
                    humidity_pct=52.0,
                    weather_condition="Hot & Dry"
                ),
                DailyForecast(
                    date=(today + timedelta(days=1)).strftime("%Y-%m-%d"),
                    temp_max_c=40.8, # Extreme heat trigger (>39°C)
                    temp_min_c=28.5,
                    rainfall_mm=0.0,
                    humidity_pct=45.0,
                    weather_condition="Heatwave Condition"
                ),
                DailyForecast(
                    date=(today + timedelta(days=2)).strftime("%Y-%m-%d"),
                    temp_max_c=39.5,
                    temp_min_c=28.0,
                    rainfall_mm=0.0,
                    humidity_pct=48.0,
                    weather_condition="Intense Sunlight"
                ),
                DailyForecast(
                    date=(today + timedelta(days=3)).strftime("%Y-%m-%d"),
                    temp_max_c=37.0,
                    temp_min_c=26.5,
                    rainfall_mm=4.0,
                    humidity_pct=60.0,
                    weather_condition="Isolated Heat Thunderstorm"
                ),
                DailyForecast(
                    date=(today + timedelta(days=4)).strftime("%Y-%m-%d"),
                    temp_max_c=36.0,
                    temp_min_c=26.0,
                    rainfall_mm=0.0,
                    humidity_pct=58.0,
                    weather_condition="Clear Sky"
                ),
            ]
        else:
            # General balanced scenario
            forecasts = [
                DailyForecast(
                    date=(today + timedelta(days=i)).strftime("%Y-%m-%d"),
                    temp_max_c=33.0 + (i * 0.8),
                    temp_min_c=24.0 + (i * 0.3),
                    rainfall_mm=8.0 if i == 2 else 1.5,
                    humidity_pct=72.0 - (i * 2),
                    weather_condition="Partly Cloudy" if i != 2 else "Passing Showers"
                )
                for i in range(5)
            ]

        return WeatherForecastResponse(
            location=location.title(),
            source="DEMO Simulated Weather Engine (Tamil Nadu Agromet Dataset)",
            period=f"{forecasts[0].date} to {forecasts[-1].date} (5-Day Window)",
            is_demo=True,
            daily_forecasts=forecasts
        )

class OpenMeteoWeatherProvider(BaseWeatherProvider):
    """
    Live Weather Provider using Open-Meteo's free, public API.
    Does not require any API keys.
    """
    async def get_forecast(self, location: str) -> WeatherForecastResponse:
        loc_key = location.strip().lower()
        coords = None

        # Look up known district coordinates
        for key, val in TAMIL_NADU_DISTRICTS.items():
            if key in loc_key:
                coords = (val["lat"], val["lon"], val["name"])
                break

        # If not in local table, use Open-Meteo Geocoding
        if not coords:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    geo_res = await client.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": location, "count": 1, "language": "en", "format": "json"}
                    )
                    if geo_res.status_code == 200:
                        results = geo_res.json().get("results")
                        if results:
                            coords = (results[0]["latitude"], results[0]["longitude"], results[0]["name"])
            except Exception:
                pass

        # Fallback to Thanjavur coordinates if geocoding fails
        if not coords:
            coords = (10.7870, 79.1378, f"{location.title()} (Estimated)")

        lat, lon, resolved_name = coords

        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                        "timezone": "Asia/Kolkata",
                        "forecast_days": 5
                    }
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=503,
                detail=f"Open-Meteo weather service timed out while fetching forecast for '{location}'."
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Open-Meteo weather service connection error: {exc}"
            )
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to communicate with Open-Meteo weather service: {exc}"
            )

        if res.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Open-Meteo weather API returned error HTTP {res.status_code}: {res.text}"
            )

        data = res.json().get("daily", {})
        dates = data.get("time", [])
        max_temps = data.get("temperature_2m_max", [])
        min_temps = data.get("temperature_2m_min", [])
        rains = data.get("precipitation_sum", [])

        if not dates:
            raise HTTPException(
                status_code=502,
                detail=f"No forecast data returned by Open-Meteo weather service for '{location}'."
            )

        forecasts = []
        for i in range(len(dates)):
            rain = float(rains[i]) if i < len(rains) and rains[i] is not None else 0.0
            t_max = float(max_temps[i]) if i < len(max_temps) and max_temps[i] is not None else 32.0
            t_min = float(min_temps[i]) if i < len(min_temps) and min_temps[i] is not None else 24.0

            condition = "Clear"
            if rain > 40:
                condition = "Heavy Rain"
            elif rain > 15:
                condition = "Moderate Rain"
            elif rain > 2:
                condition = "Light Rain"
            elif t_max > 38:
                condition = "Extreme Heat"
            else:
                condition = "Partly Cloudy"

            forecasts.append(DailyForecast(
                date=dates[i],
                temp_max_c=t_max,
                temp_min_c=t_min,
                rainfall_mm=rain,
                humidity_pct=75.0,
                weather_condition=condition
            ))

        return WeatherForecastResponse(
            location=resolved_name,
            source="Open-Meteo Live API (Free Tier)",
            period=f"{forecasts[0].date} to {forecasts[-1].date} (5-Day Window)",
            is_demo=False,
            daily_forecasts=forecasts
        )

def get_weather_provider() -> BaseWeatherProvider:
    """Factory selecting the configured weather provider."""
    if settings.WEATHER_PROVIDER == "open_meteo":
        return OpenMeteoWeatherProvider()
    return DemoWeatherProvider()
