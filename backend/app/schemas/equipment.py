"""Pydantic schemas for equipment."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EquipmentBase(BaseModel):
    plant_id: int
    name: str
    code: Optional[str] = None
    equipment_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    power_kw: Optional[float] = None
    status: str = "active"
    install_date: Optional[datetime] = None
    notes: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    equipment_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    power_kw: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class EquipmentResponse(EquipmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EquipmentHoursBase(BaseModel):
    equipment_id: int
    date: datetime
    hours_run: float
    energy_kwh: Optional[float] = None
    notes: Optional[str] = None


class EquipmentHoursCreate(EquipmentHoursBase):
    pass


class EquipmentHoursResponse(EquipmentHoursBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
