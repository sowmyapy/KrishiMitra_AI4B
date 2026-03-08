"""
Farmer and Farm Plot models
"""
import uuid
from datetime import datetime

from sqlalchemy import DECIMAL, Column, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.config.database import Base
from src.config.db_types import ARRAY, UUID, Geography


class Farmer(Base):
    """Farmer model"""
    __tablename__ = "farmers"

    farmer_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    preferred_language = Column(String(10), nullable=False)
    timezone = Column(String(50), nullable=False)
    registration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farm_plots = relationship("FarmPlot", back_populates="farmer", cascade="all, delete-orphan")
    advisories = relationship("Advisory", back_populates="farmer")
    call_records = relationship("CallRecord", back_populates="farmer")
    chatbot_sessions = relationship("ChatbotSession", back_populates="farmer")

    def __repr__(self):
        return f"<Farmer(id={self.farmer_id}, phone={self.phone_number})>"


class FarmPlot(Base):
    """Farm Plot model"""
    __tablename__ = "farm_plots"

    plot_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(), ForeignKey("farmers.farmer_id", ondelete="CASCADE"), nullable=False, index=True)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    area_hectares = Column(DECIMAL(10, 2), nullable=False)
    crop_types = Column(ARRAY(String), nullable=False)
    planting_date = Column(Date)
    expected_harvest_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer = relationship("Farmer", back_populates="farm_plots")
    crop_health_indicators = relationship("CropHealthIndicator", back_populates="farm_plot")
    stress_predictions = relationship("StressPrediction", back_populates="farm_plot")
    advisories = relationship("Advisory", back_populates="farm_plot")

    def __repr__(self):
        return f"<FarmPlot(id={self.plot_id}, farmer_id={self.farmer_id}, area={self.area_hectares}ha)>"
