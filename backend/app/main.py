"""
PTAS Backend - FastAPI Main Application
Sistema de Gestión para Plantas de Tratamiento de Aguas Servidas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.routers import (
    auth_router,
    plants_router,
    measurements_router,
    equipment_router,
    alerts_router,
    dashboard_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    print("🚀 Starting PTAS Backend...")
    init_db()
    
    # Create default admin user
    from app.core.database import SessionLocal
    from app.models.user import User
    from app.models.plant import Plant
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create default plant first
            plant = Plant(
                name="PTAS demo",
                code="PTAS-001",
                address="Demo",
                region="Metropolitana",
                capacity_m3d=500,
                population_equiv=2000,
                treatment_type="Lodos Activados",
                status="active"
            )
            db.add(plant)
            db.flush()  # Get plant.id
            
            # Create default admin
            admin = User(
                email="admin@ptas.cl",
                username="admin",
                password_hash=get_password_hash("admin123"),
                full_name="Administrador PTAS",
                role="administrador",
                is_active=True,
                plant_id=plant.id
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin user created: admin / admin123")
    except Exception as e:
        print(f"⚠️ Error creating default data: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield
    
    # Shutdown
    print("🛑 Shutting down PTAS Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de Gestión para Plantas de Tratamiento de Aguas Servidas - Chile",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(plants_router, prefix="/api/v1")
app.include_router(measurements_router, prefix="/api/v1")
app.include_router(equipment_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
