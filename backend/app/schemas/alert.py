"""Pydantic schemas for alerts."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertBase(BaseModel):
    plant_id: int
    alert_type: str
    severity: str
    title: str
    message: str
    ds90_violation: bool = False
    ds609_violation: bool = False
    norm_reference: Optional[str] = None


class AlertCreate(AlertBase):
    measurement_id: Optional[int] = None
    equipment_id: Optional[int] = None


class AlertUpdate(BaseModel):
    is_resolved: Optional[str] = None
    resolution_notes: Optional[str] = None


class AlertResolve(BaseModel):
    resolution_notes: Optional[str] = None


class AlertResponse(AlertBase):
    id: int
    measurement_id: Optional[int] = None
    equipment_id: Optional[int] = None
    is_resolved: str
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertStats(BaseModel):
    """Alert statistics."""
    total: int = 0
    active: int = 0
    resolved: int = 0
    critical: int = 0
    warning: int = 0
    ds90_violations: int = 0
    ds609_violations: int = 0
