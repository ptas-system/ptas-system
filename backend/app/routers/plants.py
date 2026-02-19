"""
Plants router - CRUD operations for PTAS plants.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantUpdate, PlantResponse

router = APIRouter(prefix="/plants", tags=["Plants"])


@router.get("", response_model=List[PlantResponse])
def get_plants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all plants."""
    plants = db.query(Plant).offset(skip).limit(limit).all()
    return plants


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific plant by ID."""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planta no encontrada"
        )
    return plant


@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_plant(
    plant_data: PlantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["administrador"]))
):
    """Create a new plant (admin only)."""
    # Check if code already exists
    if db.query(Plant).filter(Plant.code == plant_data.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de planta ya existe"
        )
    
    plant = Plant(**plant_data.model_dump())
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant


@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(
    plant_id: int,
    plant_data: PlantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["administrador", "supervisor"]))
):
    """Update a plant."""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planta no encontrada"
        )
    
    # Check code uniqueness if changing
    if plant_data.code and plant_data.code != plant.code:
        if db.query(Plant).filter(Plant.code == plant_data.code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de planta ya existe"
            )
    
    for key, value in plant_data.model_dump(exclude_unset=True).items():
        setattr(plant, key, value)
    
    db.commit()
    db.refresh(plant)
    return plant


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["administrador"]))
):
    """Delete (deactivate) a plant."""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planta no encontrada"
        )
    
    # Soft delete
    plant.status = "inactive"
    db.commit()
    return None
