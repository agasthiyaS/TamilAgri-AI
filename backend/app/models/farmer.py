from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class Farmer(Base):
    """
    Farmer profile table storing agricultural details and alert preferences.
    """
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False, index=True)
    location = Column(String(100), nullable=False) # e.g., Thanjavur, Madurai, Tiruchirappalli
    crop = Column(String(50), nullable=False, default="Paddy")
    growth_stage = Column(String(50), nullable=False, default="Nursery") # Nursery, Tillering, Flowering, Grain filling, Harvest
    preferred_language = Column(String(10), nullable=False, default="ta") # 'ta' (Tamil) or 'en' (English)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
