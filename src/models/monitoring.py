"""
Monitoring and Prediction models
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Integer, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from src.config.database import Base
from src.config.db_types import UUID, ARRAY


class StressType(enum.Enum):
    """Crop stress types"""
    DROUGHT = "drought"
    PEST_INFESTATION = "pest"
    DISEASE = "disease"
    FLOODING = "flooding"
    NUTRIENT_DEFICIENCY = "nutrient"
    UNKNOWN = "unknown"


class CropHealthIndicator(Base):
    """Crop Health Indicators model"""
    __tablename__ = "crop_health_indicators"
    
    indicator_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farm_plot_id = Column(UUID(), ForeignKey("farm_plots.plot_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # NDVI metrics
    ndvi_mean = Column(DECIMAL(5, 3))  # -1 to 1
    ndvi_std = Column(DECIMAL(5, 3))
    
    # Moisture and vegetation
    moisture_level = Column(DECIMAL(5, 2))  # 0 to 100 (percentage)
    vegetation_index = Column(DECIMAL(5, 3))
    
    # Weather data
    temperature_celsius = Column(DECIMAL(5, 2))
    rainfall_mm = Column(DECIMAL(6, 2))
    
    # Metadata
    data_source = Column(String(20), nullable=False)  # 'satellite' or 'weather'
    quality_score = Column(DECIMAL(3, 2))  # 0 to 1
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm_plot = relationship("FarmPlot", back_populates="crop_health_indicators")
    
    def __repr__(self):
        return f"<CropHealthIndicator(plot_id={self.farm_plot_id}, timestamp={self.timestamp}, ndvi={self.ndvi_mean})>"


class StressPrediction(Base):
    """Stress Prediction model"""
    __tablename__ = "stress_predictions"
    
    prediction_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farm_plot_id = Column(UUID(), ForeignKey("farm_plots.plot_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Prediction results
    risk_score = Column(DECIMAL(5, 2), nullable=False)  # 0 to 100
    stress_type = Column(SQLEnum(StressType), nullable=False)
    confidence = Column(DECIMAL(3, 2), nullable=False)  # 0 to 1
    days_to_critical = Column(Integer)
    
    # Contributing factors
    contributing_factors = Column(ARRAY(String))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm_plot = relationship("FarmPlot", back_populates="stress_predictions")
    advisories = relationship("Advisory", back_populates="prediction")
    
    def __repr__(self):
        return f"<StressPrediction(plot_id={self.farm_plot_id}, risk={self.risk_score}, type={self.stress_type.value})>"
