from fastapi import APIRouter
from app.api.v1.endpoints import auth, vehicles, telemetry

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry & Analytics"])