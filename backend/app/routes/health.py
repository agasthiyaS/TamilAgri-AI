from fastapi import APIRouter
from ..config import settings

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def health_check():
    """Health check endpoint displaying system state and demo status."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE,
        "weather_provider": settings.WEATHER_PROVIDER,
        "sms_provider": settings.SMS_PROVIDER,
        "mode_notice": "DEMO MODE ACTIVE: Weather data is simulated and SMS alerts are safely logged." if settings.DEMO_MODE else "PRODUCTION MODE"
    }
