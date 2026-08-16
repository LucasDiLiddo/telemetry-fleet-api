from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from app.api.deps import DbDep, get_current_user, get_current_active_admin
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services.vehicle_service import VehicleService

router = APIRouter()


@router.get("/", response_model=list[VehicleResponse])
def list_vehicles(
    db: DbDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None
):
    """Listar vehículos de la flota (Accesible para cualquier usuario autenticado)."""
    return VehicleService.get_all(db, skip=skip, limit=limit, status_filter=status)


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_in: VehicleCreate,
    db: DbDep,
    admin_user: Annotated[User, Depends(get_current_active_admin)]
):
    """Registrar un nuevo vehículo en la flota (Solo Administradores)."""
    return VehicleService.create(db, vehicle_in)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: DbDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Obtener detalle de un vehículo por ID."""
    return VehicleService.get_by_id(db, vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: DbDep,
    admin_user: Annotated[User, Depends(get_current_active_admin)]
):
    """Actualizar datos o estado de un vehículo (Solo Administradores)."""
    return VehicleService.update(db, vehicle_id, vehicle_in)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: DbDep,
    admin_user: Annotated[User, Depends(get_current_active_admin)]
):
    """Eliminar un vehículo de la flota (Solo Administradores)."""
    VehicleService.delete(db, vehicle_id)