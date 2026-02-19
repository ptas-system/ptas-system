"""
Equipment model - Equipment in the PTAS.
"""
from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Equipment(Base):
    """Equipment model - machinery and equipment in the plant."""
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)
    equipment_type = Column(String(100), nullable=False)
    # Types: bomba, motor, soplador, mezclador, decantador, filtro, otro
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    power_kw = Column(Numeric(6, 2), nullable=True)
    status = Column(String(50), default="active")  # active, inactive, maintenance, broken
    install_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    plant = relationship("Plant", back_populates="equipment")
    hours = relationship("EquipmentHours", back_populates="equipment")


class EquipmentHours(Base):
    """Equipment operating hours."""
    __tablename__ = "equipment_hours"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    hours_run = Column(Numeric(5, 2), nullable=False)
    energy_kwh = Column(Numeric(10, 2), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    equipment = relationship("Equipment", back_populates="hours")
