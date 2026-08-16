from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from app.api.deps import DbDep, get_current_user
from app.models.user import User
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse, TelemetryStats
from app.services.telemetry_service import TelemetryService

router = APIRouter()


@router.post("/", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
def ingest_telemetry(
    data_in: TelemetryCreate,
    db: DbDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Ingesta de eventos y métricas de un vehículo en tiempo real."""
    return TelemetryService.record_event(db, data_in)


@router.get("/{vehicle_id}/history", response_model=list[TelemetryResponse])
def get_history(
    vehicle_id: int,
    db: DbDep,
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(30, ge=1, le=100)
):
    """Obtiene el historial cronológico de registros de un vehículo."""
    return TelemetryService.get_vehicle_history(db, vehicle_id, limit=limit)


@router.get("/{vehicle_id}/stats", response_model=TelemetryStats)
def get_stats(
    vehicle_id: int,
    db: DbDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Métricas agregadas: promedio de velocidad, velocidad máxima, combustible actual y temp promedio."""
    return TelemetryService.get_vehicle_stats(db, vehicle_id)