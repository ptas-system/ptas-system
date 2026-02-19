"""
Measurement model - Operational data from PTAS.
"""
from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Measurement(Base):
    """Measurement model - operational data from the plant."""
    __tablename__ = "measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Process phase
    phase = Column(String(50), nullable=False)
    # Options: afluente, pretratamiento, reactor, clarificador, desinfeccion, lodos
    
    # Hydraulic parameters
    caudal_affluent_m3h = Column(Numeric(10, 3), nullable=True)  # Inflow
    caudal_effluent_m3h = Column(Numeric(10, 3), nullable=True)  # Outflow
    
    # Physical parameters
    ph = Column(Numeric(5, 2), nullable=True)
    temperature = Column(Numeric(5, 2), nullable=True)
    conductivity = Column(Numeric(10, 2), nullable=True)
    turbidity = Column(Numeric(10, 2), nullable=True)
    
    # Chemical parameters
    od = Column(Numeric(6, 2), nullable=True)  # Dissolved Oxygen
    chlorine_free = Column(Numeric(6, 2), nullable=True)
    
    # Organic parameters
    sst = Column(Numeric(10, 2), nullable=True)  # Total Suspended Solids
    dbo5 = Column(Numeric(10, 2), nullable=True)
    dqo = Column(Numeric(10, 2), nullable=True)
    
    # Sludge
    level_sludge_m = Column(Numeric(5, 3), nullable=True)
    
    # Notes and validation
    notes = Column(Text, nullable=True)
    validated = Column(String(10), default="pending")  # pending, validated, rejected
    validated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    plant = relationship("Plant", back_populates="measurements")

    # User who created the measurement
    user = relationship(
        "User",
        back_populates="measurements",
        foreign_keys=[user_id],
    )

    # User who validated the measurement (optional)
    validator = relationship(
        "User",
        back_populates="validated_measurements",
        foreign_keys=[validated_by],
    )

    alerts = relationship("Alert", back_populates="measurement")
