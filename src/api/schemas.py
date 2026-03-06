"""
Pydantic schemas for API requests and responses
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from uuid import UUID


# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


# Farmer schemas
class FarmerCreate(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    preferred_language: str = Field(..., min_length=2, max_length=10)
    timezone: str = Field(default="Asia/Kolkata")


class FarmerResponse(BaseModel):
    farmer_id: UUID
    phone_number: str
    preferred_language: str
    timezone: str
    registration_date: datetime
    
    class Config:
        from_attributes = True


# Farm Plot schemas
class FarmPlotCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    area_hectares: float = Field(..., gt=0)
    crop_types: List[str]
    planting_date: Optional[date] = None
    expected_harvest_date: Optional[date] = None


class FarmPlotResponse(BaseModel):
    plot_id: UUID
    farmer_id: UUID
    area_hectares: float
    crop_types: List[str]
    planting_date: Optional[date]
    expected_harvest_date: Optional[date]
    
    class Config:
        from_attributes = True


# Advisory schemas
class AdvisoryResponse(BaseModel):
    advisory_id: UUID
    farmer_id: UUID
    farm_plot_id: UUID
    stress_type: str
    urgency_level: str
    actions: list
    created_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True


class AdvisoryCreate(BaseModel):
    farmer_id: UUID
    plot_id: UUID
    stress_type: str
    risk_score: float
    advisory_text: str
    language: str = "en"


# Call Record schemas
class CallRecordResponse(BaseModel):
    call_id: UUID
    farmer_id: UUID
    call_type: str
    status: str
    duration_seconds: Optional[int]
    initiated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Chatbot Session schemas
class ChatbotSessionResponse(BaseModel):
    session_id: UUID
    farmer_id: UUID
    language: str
    started_at: datetime
    ended_at: Optional[datetime]
    turn_count: int
    
    class Config:
        from_attributes = True


class ConversationTurnCreate(BaseModel):
    session_id: UUID
    user_input: str
    bot_response: str
    intent: Optional[str] = None


# Health check schema
class HealthCheck(BaseModel):
    status: str
    version: str
    timestamp: datetime


# Error schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Pagination schema
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


# Crop health indicator schema
class CropHealthIndicatorResponse(BaseModel):
    indicator_id: UUID
    plot_id: UUID
    ndvi_mean: float
    ndvi_std: float
    moisture_level: float
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Stress prediction schema
class StressPredictionResponse(BaseModel):
    prediction_id: UUID
    plot_id: UUID
    stress_type: str
    risk_score: float
    confidence: float
    predicted_at: datetime
    
    class Config:
        from_attributes = True


# Voice call request schema
class VoiceCallRequest(BaseModel):
    farmer_id: UUID
    call_type: str = Field(..., pattern="^(advisory|chatbot)$")
    message: Optional[str] = None
    language: Optional[str] = "en"


# Chatbot message schema
class ChatbotMessage(BaseModel):
    session_id: Optional[str] = None
    farmer_id: UUID
    message: str
    language: str = "en"


class ChatbotResponse(BaseModel):
    session_id: str
    response: str
    intent: str
    confidence: float
    should_end: bool
