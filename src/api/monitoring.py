"""
Monitoring API endpoints
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.services.monitoring import auto_monitor_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


class MonitoringSettings(BaseModel):
    """Monitoring settings model"""
    check_interval: Optional[int] = None
    risk_threshold: Optional[float] = None
    call_threshold: Optional[float] = None


@router.post("/start")
async def start_monitoring():
    """Start automated monitoring service"""
    try:
        await auto_monitor_service.start_monitoring()
        return {
            "status": "success",
            "message": "Monitoring service started",
            "monitoring_status": auto_monitor_service.get_status()
        }
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_monitoring():
    """Stop automated monitoring service"""
    try:
        await auto_monitor_service.stop_monitoring()
        return {
            "status": "success",
            "message": "Monitoring service stopped",
            "monitoring_status": auto_monitor_service.get_status()
        }
    except Exception as e:
        logger.error(f"Failed to stop monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_monitoring_status():
    """Get monitoring service status"""
    return auto_monitor_service.get_status()


@router.put("/settings")
async def update_monitoring_settings(settings: MonitoringSettings):
    """Update monitoring settings"""
    try:
        settings_dict = settings.dict(exclude_none=True)
        auto_monitor_service.update_settings(settings_dict)
        
        return {
            "status": "success",
            "message": "Settings updated",
            "monitoring_status": auto_monitor_service.get_status()
        }
    except Exception as e:
        logger.error(f"Failed to update settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-now")
async def trigger_immediate_check():
    """Trigger an immediate check of all farmers"""
    try:
        if not auto_monitor_service.is_running:
            raise HTTPException(
                status_code=400,
                detail="Monitoring service is not running. Start it first."
            )
        
        # Trigger immediate check by calling the check method
        await auto_monitor_service._check_all_farmers()
        
        return {
            "status": "success",
            "message": "Immediate check completed",
            "monitoring_status": auto_monitor_service.get_status()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger check: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-stats")
async def reset_statistics():
    """Reset monitoring statistics"""
    try:
        auto_monitor_service.monitoring_stats = {
            "started_at": auto_monitor_service.monitoring_stats.get("started_at"),
            "last_check": None,
            "total_checks": 0,
            "farmers_monitored": 0,
            "advisories_generated": 0,
            "calls_made": 0,
            "errors": 0
        }
        
        return {
            "status": "success",
            "message": "Statistics reset",
            "monitoring_status": auto_monitor_service.get_status()
        }
    except Exception as e:
        logger.error(f"Failed to reset statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
