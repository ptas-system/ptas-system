"""
Alerts router - CRUD operations for alerts.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResolve,
    AlertResponse,
    AlertStats,
)

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    plant_id: Optional[int] = None,
    is_resolved: Optional[str] = None,
    severity: Optional[str] = None,
    alert_type: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alerts with filters."""
    query = db.query(Alert)
    
    if plant_id:
        query = query.filter(Alert.plant_id == plant_id)
    elif current_user.role == "operador" and current_user.plant_id:
        query = query.filter(Alert.plant_id == current_user.plant_id)
    
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    if severity:
        query = query.filter(Alert.severity == severity)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    
    return query.order_by(Alert.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/stats", response_model=AlertStats)
def get_alert_stats(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert statistics."""
    alerts = db.query(Alert).filter(Alert.plant_id == plant_id).all()
    
    if not alerts:
        return AlertStats()
    
    active = sum(1 for a in alerts if a.is_resolved == "false")
    resolved = sum(1 for a in alerts if a.is_resolved == "true")
    critical = sum(1 for a in alerts if a.severity == "critical" and a.is_resolved == "false")
    warning = sum(1 for a in alerts if a.severity == "warning" and a.is_resolved == "false")
    ds90 = sum(1 for a in alerts if a.ds90_violation)
    ds609 = sum(1 for a in alerts if a.ds609_violation)
    
    return AlertStats(
        total=len(alerts),
        active=active,
        resolved=resolved,
        critical=critical,
        warning=warning,
        ds90_violations=ds90,
        ds609_violations=ds609
    )


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific alert by ID."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )
    return alert


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new alert."""
    alert = Alert(**alert_data.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    resolve_data: AlertResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Resolve an alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )
    
    alert.is_resolved = "true"
    alert.resolved_by = current_user.id
    alert.resolved_at = datetime.now()
    alert.resolution_notes = resolve_data.resolution_notes
    
    db.commit()
    db.refresh(alert)
    return alert