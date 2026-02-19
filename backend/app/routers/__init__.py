"""API routers package."""
from app.routers.auth import router as auth_router
from app.routers.plants import router as plants_router
from app.routers.measurements import router as measurements_router
from app.routers.equipment import router as equipment_router
from app.routers.alerts import router as alerts_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "plants_router",
    "measurements_router",
    "equipment_router",
    "alerts_router",
    "dashboard_router",
]