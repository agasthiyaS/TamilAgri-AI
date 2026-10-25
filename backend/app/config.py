import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root or backend folder
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "backend" / ".env")

class Settings:
    PROJECT_NAME: str = "TamilAgri AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Crop-Specific Climate Risk Analysis & Multilingual SMS Early Warning System"
    
    # Execution mode (Runs without API keys by default)
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    # Server settings
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    ALLOWED_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tamilagri.db")
    
    # Weather provider adapter ("demo" or "open_meteo")
    WEATHER_PROVIDER: str = os.getenv("WEATHER_PROVIDER", "demo").lower()
    
    # SMS gateway adapter ("demo", "twilio", or "generic_webhook")
    SMS_PROVIDER: str = os.getenv("SMS_PROVIDER", "demo").lower()
    
    # Optional credentials for live SMS gateways
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER", "")
    SMS_WEBHOOK_URL: str = os.getenv("SMS_WEBHOOK_URL", "")

settings = Settings()
