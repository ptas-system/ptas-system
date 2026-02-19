"""Pydantic schemas for plant."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PlantBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    region: Optional[str] = None
    capacity_m3d: Optional[int] = None
    population_equiv: Optional[int] = None
    treatment_type: Optional[str] = None
    status: str = "active"
    ds90_enabled: bool = True
    ds609_enabled: bool = True


class PlantCreate(PlantBase):
    pass


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    capacity_m3d: Optional[int] = None
    population_equiv: Optional[int] = None
    treatment_type: Optional[str] = None
    status: Optional[str] = None
    ds90_enabled: Optional[bool] = None
    ds609_enabled: Optional[bool] = None


class PlantResponse(PlantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
