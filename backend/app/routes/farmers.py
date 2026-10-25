from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.farmer import Farmer
from ..schemas.farmer import FarmerCreate, FarmerResponse

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.post("", response_model=FarmerResponse, status_code=status.HTTP_201_CREATED)
def register_farmer(farmer_in: FarmerCreate, db: Session = Depends(get_db)):
    """Registers a new farmer with phone validation and crop stage preferences."""
    farmer = Farmer(
        name=farmer_in.name.strip(),
        mobile_number=farmer_in.mobile_number,
        location=farmer_in.location.strip(),
        crop=farmer_in.crop,
        growth_stage=farmer_in.growth_stage,
        preferred_language=farmer_in.preferred_language
    )
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    return farmer

@router.get("", response_model=List[FarmerResponse])
def list_farmers(db: Session = Depends(get_db)):
    """Lists all registered farmers."""
    return db.query(Farmer).order_by(Farmer.created_at.desc()).all()

@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Retrieves a single farmer profile by ID."""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Deletes a farmer profile."""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    db.delete(farmer)
    db.commit()
    return None
