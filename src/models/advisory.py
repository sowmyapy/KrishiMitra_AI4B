"""
Advisory and Action models
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from src.config.database import Base
from src.config.db_types import UUID, ARRAY, JSONB


class UrgencyLevel(enum.Enum):
    """Advisory urgency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Advisory(Base):
    """Advisory model"""
    __tablename__ = "advisories"
    
    advisory_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(), ForeignKey("stress_predictions.prediction_id"), index=True)
    farm_plot_id = Column(UUID(), ForeignKey("farm_plots.plot_id", ondelete="CASCADE"), nullable=False, index=True)
    farmer_id = Column(UUID(), ForeignKey("farmers.farmer_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Advisory content
    advisory_text = Column(Text, nullable=True)  # Full advisory message text
    stress_type = Column(String(20), nullable=False)
    urgency_level = Column(SQLEnum(UrgencyLevel), nullable=False)
    risk_score = Column(Float, nullable=True)  # Risk score (0-100)
    actions = Column(JSONB, nullable=False)  # List of actions with details
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    
    # Relationships
    prediction = relationship("StressPrediction", back_populates="advisories")
    farm_plot = relationship("FarmPlot", back_populates="advisories")
    farmer = relationship("Farmer", back_populates="advisories")
    call_records = relationship("CallRecord", back_populates="advisory")
    
    def __repr__(self):
        return f"<Advisory(id={self.advisory_id}, farmer_id={self.farmer_id}, urgency={self.urgency_level.value})>"


class Action(Base):
    """Action model (for structured action storage if needed)"""
    __tablename__ = "actions"
    
    action_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    advisory_id = Column(UUID(), ForeignKey("advisories.advisory_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Action details
    description = Column(Text, nullable=False)
    timing = Column(String(50), nullable=False)  # "immediately", "within 24 hours", etc.
    priority = Column(Integer, nullable=False)  # 1 (highest) to 5 (lowest)
    resources_required = Column(JSONB)  # List of resources
    expected_outcome = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Action(id={self.action_id}, priority={self.priority})>"


class Resource(Base):
    """Resource model (for structured resource storage if needed)"""
    __tablename__ = "resources"
    
    resource_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    action_id = Column(UUID(), ForeignKey("actions.action_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Resource details
    resource_type = Column(String(50), nullable=False)  # "water", "fertilizer", "pesticide"
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # "liters", "kg", "ml"
    specific_product = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Resource(type={self.resource_type}, quantity={self.quantity} {self.unit})>"
