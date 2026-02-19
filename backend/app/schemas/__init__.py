"""Pydantic schemas package."""
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.schemas.plant import (
    PlantCreate,
    PlantUpdate,
    PlantResponse,
)
from app.schemas.measurement import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementResponse,
    MeasurementStats,
)
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
    EquipmentHoursCreate,
    EquipmentHoursResponse,
)
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResolve,
    AlertResponse,
    AlertStats,
)

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "PlantCreate",
    "PlantUpdate",
    "PlantResponse",
    "MeasurementCreate",
    "MeasurementUpdate",
    "MeasurementResponse",
    "MeasurementStats",
    "EquipmentCreate",
    "EquipmentUpdate",
    "EquipmentResponse",
    "EquipmentHoursCreate",
    "EquipmentHoursResponse",
    "AlertCreate",
    "AlertUpdate",
    "AlertResolve",
    "AlertResponse",
    "AlertStats",
]
