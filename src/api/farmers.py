"""
Farmer management API endpoints
"""
import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.farmer import Farmer, FarmPlot
from src.api.schemas import (
    FarmerCreate,
    FarmerResponse,
    FarmPlotCreate,
    FarmPlotResponse
)
from src.api.auth import get_current_user, require_staff

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/farmers", tags=["farmers"])


@router.post("/", response_model=FarmerResponse, status_code=status.HTTP_201_CREATED)
async def create_farmer(
    farmer_data: FarmerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new farmer"""
    
    # Check if phone number already exists
    existing = db.query(Farmer).filter(
        Farmer.phone_number == farmer_data.phone_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Create farmer
    farmer = Farmer(
        phone_number=farmer_data.phone_number,
        preferred_language=farmer_data.preferred_language,
        timezone=farmer_data.timezone
    )
    
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    
    logger.info(f"Created farmer {farmer.farmer_id}")
    return farmer


@router.get("/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get farmer by ID"""
    
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    return farmer


@router.get("/", response_model=List[FarmerResponse])
async def list_farmers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """List all farmers (staff only)"""
    
    farmers = db.query(Farmer).offset(skip).limit(limit).all()
    return farmers


@router.put("/{farmer_id}", response_model=FarmerResponse)
async def update_farmer(
    farmer_id: UUID,
    farmer_data: FarmerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update farmer information"""
    
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    # Update fields
    farmer.preferred_language = farmer_data.preferred_language
    farmer.timezone = farmer_data.timezone
    
    db.commit()
    db.refresh(farmer)
    
    logger.info(f"Updated farmer {farmer_id}")
    return farmer


@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farmer(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Delete farmer (staff only)"""
    
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    db.delete(farmer)
    db.commit()
    
    logger.info(f"Deleted farmer {farmer_id}")


# Farm Plot endpoints

@router.post("/{farmer_id}/plots", response_model=FarmPlotResponse, status_code=status.HTTP_201_CREATED)
async def create_farm_plot(
    farmer_id: UUID,
    plot_data: FarmPlotCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new farm plot"""
    
    # Verify farmer exists
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    # Create plot
    plot = FarmPlot(
        farmer_id=farmer_id,
        location=f"POINT({plot_data.longitude} {plot_data.latitude})",
        area_hectares=plot_data.area_hectares,
        crop_types=plot_data.crop_types,
        planting_date=plot_data.planting_date,
        expected_harvest_date=plot_data.expected_harvest_date
    )
    
    db.add(plot)
    db.commit()
    db.refresh(plot)
    
    logger.info(f"Created plot {plot.plot_id} for farmer {farmer_id}")
    return plot


@router.get("/{farmer_id}/plots", response_model=List[FarmPlotResponse])
async def list_farmer_plots(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all plots for a farmer"""
    
    plots = db.query(FarmPlot).filter(FarmPlot.farmer_id == farmer_id).all()
    return plots


@router.get("/{farmer_id}/plots/{plot_id}", response_model=FarmPlotResponse)
async def get_farm_plot(
    farmer_id: UUID,
    plot_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get specific farm plot"""
    
    plot = db.query(FarmPlot).filter(
        FarmPlot.plot_id == plot_id,
        FarmPlot.farmer_id == farmer_id
    ).first()
    
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    
    return plot


@router.delete("/{farmer_id}/plots/{plot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farm_plot(
    farmer_id: UUID,
    plot_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete farm plot"""
    
    plot = db.query(FarmPlot).filter(
        FarmPlot.plot_id == plot_id,
        FarmPlot.farmer_id == farmer_id
    ).first()
    
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    
    db.delete(plot)
    db.commit()
    
    logger.info(f"Deleted plot {plot_id}")
