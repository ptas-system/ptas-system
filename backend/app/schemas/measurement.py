"""Pydantic schemas for measurement."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class MeasurementBase(BaseModel):
    plant_id: int
    timestamp: datetime
    phase: str
    # Phase options: afluente, pretratamiento, reactor, clarificador, desinfeccion, lodos


class MeasurementCreate(MeasurementBase):
    caudal_affluent_m3h: Optional[float] = None
    caudal_effluent_m3h: Optional[float] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    conductivity: Optional[float] = None
    turbidity: Optional[float] = None
    od: Optional[float] = None
    chlorine_free: Optional[float] = None
    sst: Optional[float] = None
    dbo5: Optional[float] = None
    dqo: Optional[float] = None
    level_sludge_m: Optional[float] = None
    notes: Optional[str] = None


class MeasurementUpdate(BaseModel):
    caudal_affluent_m3h: Optional[float] = None
    caudal_effluent_m3h: Optional[float] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    conductivity: Optional[float] = None
    turbidity: Optional[float] = None
    od: Optional[float] = None
    chlorine_free: Optional[float] = None
    sst: Optional[float] = None
    dbo5: Optional[float] = None
    dqo: Optional[float] = None
    level_sludge_m: Optional[float] = None
    notes: Optional[str] = None
    validated: Optional[str] = None


class MeasurementResponse(MeasurementBase):
    id: int
    user_id: int
    caudal_affluent_m3h: Optional[float] = None
    caudal_effluent_m3h: Optional[float] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    conductivity: Optional[float] = None
    turbidity: Optional[float] = None
    od: Optional[float] = None
    chlorine_free: Optional[float] = None
    sst: Optional[float] = None
    dbo5: Optional[float] = None
    dqo: Optional[float] = None
    level_sludge_m: Optional[float] = None
    notes: Optional[str] = None
    validated: str
    validated_by: Optional[int] = None
    validated_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MeasurementStats(BaseModel):
    """Statistics for measurements."""
    avg_ph: Optional[float] = None
    avg_temperature: Optional[float] = None
    avg_sst: Optional[float] = None
    avg_dbo5: Optional[float] = None
    avg_caudal: Optional[float] = None
    compliance_rate: float = 0.0
    total_measurements: int = 0
