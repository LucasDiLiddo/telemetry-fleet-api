from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle


class TelemetryRecord(Base):
    __tablename__ = "telemetry_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    speed: Mapped[float] = mapped_column(Float, nullable=False)
    fuel_level: Mapped[float] = mapped_column(Float, nullable=False)
    engine_temp: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="telemetry_logs")

    __table_args__ = (
        Index("ix_telemetry_vehicle_timestamp", "vehicle_id", "timestamp"),
    )