"""
Alert model - Alerts and notifications from the PTAS.
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Alert(Base):
    """Alert model - alerts and warnings from the system."""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=False)
    measurement_id = Column(Integer, ForeignKey("measurements.id", ondelete="SET NULL"), nullable=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True)
    
    alert_type = Column(String(50), nullable=False)
    # Types: warning, critical, info, ds90_violation, ds609_violation, anomaly, equipment
    
    severity = Column(String(20), nullable=False)
    # Severity: low, medium, high, critical
    
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Normative references
    ds90_violation = Column(Boolean, default=False)
    ds609_violation = Column(Boolean, default=False)
    norm_reference = Column(String(100), nullable=True)  # DS90 Art. 3.a, etc.
    
    # Resolution
    is_resolved = Column(String(10), default="false")  # false, true
    resolved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    plant = relationship("Plant", back_populates="alerts")
    measurement = relationship("Measurement", back_populates="alerts")
    equipment = relationship("Equipment")
    resolved_by_user = relationship("User", back_populates="alerts_resolved")
