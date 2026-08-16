from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, status_filter: str | None = None) -> list[Vehicle]:
        query = db.query(Vehicle)
        if status_filter:
            query = query.filter(Vehicle.status == status_filter)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, vehicle_id: int) -> Vehicle:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo con ID {vehicle_id} no encontrado."
            )
        return vehicle

    @staticmethod
    def create(db: Session, vehicle_in: VehicleCreate) -> Vehicle:
        # Validación de duplicados por VIN o Patente
        existing = db.query(Vehicle).filter(
            (Vehicle.vin == vehicle_in.vin) | (Vehicle.plate_number == vehicle_in.plate_number)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un vehículo registrado con el mismo VIN o número de patente."
            )
        
        vehicle = Vehicle(**vehicle_in.model_dump())
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def update(db: Session, vehicle_id: int, vehicle_in: VehicleUpdate) -> Vehicle:
        vehicle = VehicleService.get_by_id(db, vehicle_id)
        update_data = vehicle_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(vehicle, field, value)
            
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def delete(db: Session, vehicle_id: int) -> None:
        vehicle = VehicleService.get_by_id(db, vehicle_id)
        db.delete(vehicle)
        db.commit()