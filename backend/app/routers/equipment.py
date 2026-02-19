"""
Equipment router - CRUD operations for equipment and hours.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.equipment import Equipment, EquipmentHours
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
    EquipmentHoursCreate,
    EquipmentHoursResponse,
)

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("", response_model=List[EquipmentResponse])
def get_equipment(
    plant_id: Optional[int] = None,
    status: Optional[str] = None,
    equipment_type: Optional[str] = None,
    limit: int = Query(default=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment with filters."""
    query = db.query(Equipment)
    
    if plant_id:
        query = query.filter(Equipment.plant_id == plant_id)
    elif current_user.role == "operador" and current_user.plant_id:
        query = query.filter(Equipment.plant_id == current_user.plant_id)
    
    if status:
        query = query.filter(Equipment.status == status)
    if equipment_type:
        query = query.filter(Equipment.equipment_type == equipment_type)
    
    return query.offset(offset).limit(limit).all()


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_item(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific equipment by ID."""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    return equipment


@router.post("", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    equipment_data: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new equipment."""
    equipment = Equipment(**equipment_data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment_data: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update equipment."""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    for key, value in equipment_data.model_dump(exclude_unset=True).items():
        setattr(equipment, key, value)
    
    db.commit()
    db.refresh(equipment)
    return equipment


# Equipment Hours endpoints
@router.get("/{equipment_id}/hours", response_model=List[EquipmentHoursResponse])
def get_equipment_hours(
    equipment_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(default=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment hours."""
    query = db.query(EquipmentHours).filter(EquipmentHours.equipment_id == equipment_id)
    
    if start_date:
        query = query.filter(EquipmentHours.date >= start_date)
    if end_date:
        query = query.filter(EquipmentHours.date <= end_date)
    
    return query.order_by(EquipmentHours.date.desc()).limit(limit).all()


@router.post("/{equipment_id}/hours", response_model=EquipmentHoursResponse, status_code=status.HTTP_201_CREATED)
def create_equipment_hours(
    equipment_id: int,
    hours_data: EquipmentHoursCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create equipment hours record."""
    # Verify equipment exists
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado"
        )
    
    # Check if already exists for date
    existing = db.query(EquipmentHours).filter(
        EquipmentHours.equipment_id == equipment_id,
        EquipmentHours.date == hours_data.date
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe registro de horas para esta fecha"
        )
    
    hours = EquipmentHours(**hours_data.model_dump())
    db.add(hours)
    db.commit()
    db.refresh(hours)
    return hours
