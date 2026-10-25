from .health import router as health_router
from .farmers import router as farmers_router
from .weather import router as weather_router
from .risk import router as risk_router
from .alerts import router as alerts_router
from .settings import router as settings_router

__all__ = [
    "health_router",
    "farmers_router",
    "weather_router",
    "risk_router",
    "alerts_router",
    "settings_router"
]
