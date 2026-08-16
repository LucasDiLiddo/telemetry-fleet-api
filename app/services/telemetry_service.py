from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.vehicle import Vehicle
from app.models.telemetry import TelemetryRecord
from app.schemas.telemetry import TelemetryCreate, TelemetryStats


class TelemetryService:
    @staticmethod
    def record_event(db: Session, data_in: TelemetryCreate) -> TelemetryRecord:
        # Validar que el vehículo exista y esté activo
        vehicle = db.query(Vehicle).filter(Vehicle.id == data_in.vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se puede registrar telemetría: Vehículo {data_in.vehicle_id} no existe."
            )
        if vehicle.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El vehículo se encuentra en estado '{vehicle.status}' y no puede recibir telemetría activa."
            )

        record = TelemetryRecord(**data_in.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_vehicle_history(db: Session, vehicle_id: int, limit: int = 50) -> list[TelemetryRecord]:
        return (
            db.query(TelemetryRecord)
            .filter(TelemetryRecord.vehicle_id == vehicle_id)
            .order_by(TelemetryRecord.timestamp.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_vehicle_stats(db: Session, vehicle_id: int) -> TelemetryStats:
        """Cálculo analítico agregado mediante funciones SQL (AVG, MAX, COUNT)."""
        # Verificar existencia
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo con ID {vehicle_id} no encontrado."
            )

        metrics = db.query(
            func.count(TelemetryRecord.id).label("total"),
            func.avg(TelemetryRecord.speed).label("avg_speed"),
            func.max(TelemetryRecord.speed).label("max_speed"),
            func.avg(TelemetryRecord.engine_temp).label("avg_temp")
        ).filter(TelemetryRecord.vehicle_id == vehicle_id).first()

        last_record = (
            db.query(TelemetryRecord)
            .filter(TelemetryRecord.vehicle_id == vehicle_id)
            .order_by(TelemetryRecord.timestamp.desc())
            .first()
        )

        return TelemetryStats(
            vehicle_id=vehicle_id,
            total_records=metrics.total or 0,
            avg_speed=round(metrics.avg_speed or 0.0, 2),
            max_speed=round(metrics.max_speed or 0.0, 2),
            current_fuel=round(last_record.fuel_level, 2) if last_record else 0.0,
            avg_engine_temp=round(metrics.avg_temp or 0.0, 2),
            last_reported_at=last_record.timestamp if last_record else None
        )