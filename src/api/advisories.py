"""
Advisory API endpoints
"""
import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.advisory import Advisory
from src.api.schemas import AdvisoryResponse, AdvisoryCreate
from src.api.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advisories", tags=["advisories"])


@router.post("/", response_model=AdvisoryResponse, status_code=status.HTTP_201_CREATED)
async def create_advisory(
    advisory_data: AdvisoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new advisory"""
    
    advisory = Advisory(
        farmer_id=advisory_data.farmer_id,
        plot_id=advisory_data.plot_id,
        stress_type=advisory_data.stress_type,
        risk_score=advisory_data.risk_score,
        advisory_text=advisory_data.advisory_text,
        language=advisory_data.language
    )
    
    db.add(advisory)
    db.commit()
    db.refresh(advisory)
    
    logger.info(f"Created advisory {advisory.advisory_id}")
    return advisory


@router.get("/{advisory_id}", response_model=AdvisoryResponse)
async def get_advisory(
    advisory_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get advisory by ID"""
    
    advisory = db.query(Advisory).filter(
        Advisory.advisory_id == advisory_id
    ).first()
    
    if not advisory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advisory not found"
        )
    
    return advisory


@router.get("/farmer/{farmer_id}", response_model=List[AdvisoryResponse])
async def list_farmer_advisories(
    farmer_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List advisories for a farmer"""
    
    advisories = db.query(Advisory).filter(
        Advisory.farmer_id == farmer_id
    ).order_by(
        Advisory.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return advisories


@router.get("/plot/{plot_id}", response_model=List[AdvisoryResponse])
async def list_plot_advisories(
    plot_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List advisories for a plot"""
    
    advisories = db.query(Advisory).filter(
        Advisory.plot_id == plot_id
    ).order_by(
        Advisory.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return advisories


@router.patch("/{advisory_id}/delivered", response_model=AdvisoryResponse)
async def mark_advisory_delivered(
    advisory_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mark advisory as delivered"""
    
    advisory = db.query(Advisory).filter(
        Advisory.advisory_id == advisory_id
    ).first()
    
    if not advisory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advisory not found"
        )
    
    advisory.delivered = True
    db.commit()
    db.refresh(advisory)
    
    logger.info(f"Marked advisory {advisory_id} as delivered")
    return advisory
