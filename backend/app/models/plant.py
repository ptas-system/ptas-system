"""
Plant model - Represents a PTAS (Planta de Tratamiento de Aguas Servidas).
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Plant(Base):
    """Plant model - wastewater treatment plant."""
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    address = Column(Text, nullable=True)
    region = Column(String(100), nullable=True)
    capacity_m3d = Column(Integer, nullable=True)  # Capacity m3/day
    population_equiv = Column(Integer, nullable=True)  # Population equivalent
    treatment_type = Column(String(100), nullable=True)  # Treatment type
    status = Column(String(50), default="active")  # active, inactive, maintenance
    ds90_enabled = Column(Boolean, default=True)
    ds609_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="plant")
    measurements = relationship("Measurement", back_populates="plant")
    equipment = relationship("Equipment", back_populates="plant")
    alerts = relationship("Alert", back_populates="plant")
