import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Ensure Windows terminal handles Tamil unicode characters without charmap errors
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db, SessionLocal
from .models.farmer import Farmer
from .routes import (
    health_router,
    farmers_router,
    weather_router,
    risk_router,
    alerts_router,
    settings_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes SQLite schema and seeds demo farmers for immediate hackathon evaluation."""
    init_db()
    db = SessionLocal()
    try:
        # Pre-seed initial sample farmers if database is empty
        if db.query(Farmer).count() == 0:
            demo_farmers = [
                Farmer(
                    name="Selvakumar (செல்வக்குமார்)",
                    mobile_number="+919842154321",
                    location="Thanjavur",
                    crop="Paddy",
                    growth_stage="Flowering",
                    preferred_language="ta"
                ),
                Farmer(
                    name="Murugesan (முருகேசன்)",
                    mobile_number="+919443218765",
                    location="Madurai",
                    crop="Paddy",
                    growth_stage="Tillering",
                    preferred_language="ta"
                ),
                Farmer(
                    name="Karthik Rajan",
                    mobile_number="+919789012345",
                    location="Tiruchirappalli",
                    crop="Paddy",
                    growth_stage="Harvest",
                    preferred_language="en"
                ),
                Farmer(
                    name="Anandhan (ஆனந்தன்)",
                    mobile_number="+919629087123",
                    location="Thiruvarur",
                    crop="Paddy",
                    growth_stage="Nursery",
                    preferred_language="ta"
                ),
            ]
            db.add_all(demo_farmers)
            db.commit()
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS so Vite React frontend can communicate without issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS + ["*"] if settings.DEMO_MODE else settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router, prefix="/api")
app.include_router(farmers_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} Backend API",
        "documentation": "/docs",
        "demo_mode": settings.DEMO_MODE
    }
