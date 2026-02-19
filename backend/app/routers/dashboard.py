"""
Dashboard router - Summary, trends, and KPIs.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.measurement import Measurement
from app.models.equipment import Equipment
from app.models.alert import Alert

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    plant_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get dashboard summary for a plant."""
    from app.models.plant import Plant
    
    # Get plant info
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        return {"error": "Planta no encontrada"}
    
    # Get last measurement
    last_measurement = db.query(Measurement).filter(
        Measurement.plant_id == plant_id
    ).order_by(Measurement.timestamp.desc()).first()
    
    # Get active alerts
    active_alerts = db.query(Alert).filter(
        Alert.plant_id == plant_id,
        Alert.is_resolved == "false"
    ).all()
    
    # Get equipment stats
    equipment_list = db.query(Equipment).filter(Equipment.plant_id == plant_id).all()
    equipment_stats = {
        "total": len(equipment_list),
        "active": sum(1 for e in equipment_list if e.status == "active"),
        "maintenance": sum(1 for e in equipment_list if e.status == "maintenance"),
        "broken": sum(1 for e in equipment_list if e.status == "broken")
    }
    
    # Alert stats
    critical_alerts = [a for a in active_alerts if a.severity == "critical"]
    warning_alerts = [a for a in active_alerts if a.severity == "warning"]
    
    # Build response
    response = {
        "plant": {
            "id": plant.id,
            "name": plant.name,
            "code": plant.code
        },
        "last_measurement": None,
        "compliance": {
            "ds90_compliant": True,  # Will be calculated by normativity module
            "ds609_compliant": True,
            "last_violation": None
        },
        "alerts": {
            "active": len(active_alerts),
            "critical": len(critical_alerts),
            "warning": len(warning_alerts)
        },
        "equipment": equipment_stats
    }
    
    # Add last measurement if exists
    if last_measurement:
        response["last_measurement"] = {
            "timestamp": last_measurement.timestamp.isoformat(),
            "phase": last_measurement.phase,
            "caudal_effluent_m3h": float(last_measurement.caudal_effluent_m3h) if last_measurement.caudal_effluent_m3h else None,
            "ph": float(last_measurement.ph) if last_measurement.ph else None,
            "temperature": float(last_measurement.temperature) if last_measurement.temperature else None,
            "chlorine_free": float(last_measurement.chlorine_free) if last_measurement.chlorine_free else None,
            "sst": float(last_measurement.sst) if last_measurement.sst else None,
            "dbo5": float(last_measurement.dbo5) if last_measurement.dbo5 else None
        }
    
    return response


@router.get("/trends")
def get_trends(
    plant_id: int = Query(...),
    parameter: str = Query(..., description="Parameter: ph, temperature, caudal, sst, dbo5, od, chlorine"),
    days: int = Query(default=30, le=365),
    phase: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get historical trends for a parameter."""
    from datetime import timedelta
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(Measurement).filter(
        Measurement.plant_id == plant_id,
        Measurement.timestamp >= start_date
    )
    
    if phase:
        query = query.filter(Measurement.phase == phase)
    
    measurements = query.order_by(Measurement.timestamp.asc()).all()
    
    # Map parameter names to model fields
    param_map = {
        "ph": "ph",
        "temperature": "temperature",
        "caudal": "caudal_effluent_m3h",
        "sst": "sst",
        "dbo5": "dbo5",
        "od": "od",
        "chlorine": "chlorine_free"
    }
    
    field = param_map.get(parameter)
    if not field:
        return {"error": f"Parámetro '{parameter}' no válido"}
    
    # Extract data points
    data_points = []
    for m in measurements:
        value = getattr(m, field, None)
        if value is not None:
            data_points.append({
                "timestamp": m.timestamp.isoformat(),
                "value": float(value)
            })
    
    return {
        "parameter": parameter,
        "phase": phase,
        "days": days,
        "data": data_points
    }


@router.get("/kpis")
def get_kpis(
    plant_id: int = Query(...),
    days: int = Query(default=30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get KPI summary."""
    from datetime import timedelta
    from sqlalchemy import func
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get measurements in period
    measurements = db.query(Measurement).filter(
        Measurement.plant_id == plant_id,
        Measurement.timestamp >= start_date,
        Measurement.phase == "desinfeccion"
    ).all()
    
    if not measurements:
        return {
            "period_days": days,
            "total_measurements": 0,
            "compliance_rate": 0.0
        }
    
    # Calculate KPIs
    caudal_values = [m.caudal_effluent_m3h for m in measurements if m.caudal_effluent_m3h]
    ph_values = [m.ph for m in measurements if m.ph]
    chlorine_values = [m.chlorine_free for m in measurements if m.chlorine_free]
    
    validated = sum(1 for m in measurements if m.validated == "validated")
    
    return {
        "period_days": days,
        "total_measurements": len(measurements),
        "compliance_rate": round((validated / len(measurements) * 100), 2) if measurements else 0,
        "avg_caudal": round(sum(caudal_values) / len(caudal_values), 2) if caudal_values else None,
        "avg_ph": round(sum(ph_values) / len(ph_values), 2) if ph_values else None,
        "avg_chlorine": round(sum(chlorine_values) / len(chlorine_values), 2) if chlorine_values else None,
    }
