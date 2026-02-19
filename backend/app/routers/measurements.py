"""
Measurements router - CRUD operations for operational data.
"""
from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.measurement import Measurement
from app.schemas.measurement import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementResponse,
    MeasurementStats,
)

router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.get("", response_model=List[MeasurementResponse])
def get_measurements(
    plant_id: Optional[int] = None,
    phase: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    validated: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get measurements with filters."""
    query = db.query(Measurement)
    
    # Filter by plant
    if plant_id:
        query = query.filter(Measurement.plant_id == plant_id)
    elif current_user.role == "operador" and current_user.plant_id:
        query = query.filter(Measurement.plant_id == current_user.plant_id)
    
    # Filter by phase
    if phase:
        query = query.filter(Measurement.phase == phase)
    
    # Filter by date range
    if start_date:
        query = query.filter(Measurement.timestamp >= start_date)
    if end_date:
        query = query.filter(Measurement.timestamp <= end_date)
    
    # Filter by validation status
    if validated:
        query = query.filter(Measurement.validated == validated)
    
    measurements = query.order_by(Measurement.timestamp.desc()).offset(offset).limit(limit).all()
    return measurements


@router.get("/stats", response_model=MeasurementStats)
def get_measurement_stats(
    plant_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for measurements."""
    from datetime import timedelta
    from sqlalchemy import func
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get measurements in date range
    measurements = db.query(Measurement).filter(
        Measurement.plant_id == plant_id,
        Measurement.timestamp >= start_date
    ).all()
    
    if not measurements:
        return MeasurementStats(total_measurements=0, compliance_rate=0.0)
    
    # Calculate averages
    ph_values = [m.ph for m in measurements if m.ph is not None]
    temp_values = [m.temperature for m in measurements if m.temperature is not None]
    sst_values = [m.sst for m in measurements if m.sst is not None]
    dbo5_values = [m.dbo5 for m in measurements if m.dbo5 is not None]
    caudal_values = [m.caudal_effluent_m3h for m in measurements if m.caudal_effluent_m3h is not None]
    
    # Count validated measurements
    validated_count = sum(1 for m in measurements if m.validated == "validated")
    total = len(measurements)
    compliance_rate = (validated_count / total * 100) if total > 0 else 0.0
    
    return MeasurementStats(
        avg_ph=sum(ph_values) / len(ph_values) if ph_values else None,
        avg_temperature=sum(temp_values) / len(temp_values) if temp_values else None,
        avg_sst=sum(sst_values) / len(sst_values) if sst_values else None,
        avg_dbo5=sum(dbo5_values) / len(dbo5_values) if dbo5_values else None,
        avg_caudal=sum(caudal_values) / len(caudal_values) if caudal_values else None,
        compliance_rate=round(compliance_rate, 2),
        total_measurements=total
    )


@router.get("/{measurement_id}", response_model=MeasurementResponse)
def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific measurement by ID."""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada"
        )
    return measurement


@router.post("", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
def create_measurement(
    measurement_data: MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new measurement."""
    measurement = Measurement(
        **measurement_data.model_dump(),
        user_id=current_user.id
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


@router.put("/{measurement_id}", response_model=MeasurementResponse)
def update_measurement(
    measurement_id: int,
    measurement_data: MeasurementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a measurement."""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada"
        )
    
    for key, value in measurement_data.model_dump(exclude_unset=True).items():
        setattr(measurement, key, value)
    
    db.commit()
    db.refresh(measurement)
    return measurement


@router.post("/{measurement_id}/validate", response_model=MeasurementResponse)
def validate_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate a measurement (supervisor/admin only)."""
    if current_user.role not in ["supervisor", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo supervisores pueden validar mediciones"
        )
    
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medición no encontrada"
        )
    
    measurement.validated = "validated"
    measurement.validated_by = current_user.id
    measurement.validated_at = datetime.now()
    
    db.commit()
    db.refresh(measurement)
    return measurement
