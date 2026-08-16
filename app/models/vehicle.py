from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.telemetry import TelemetryRecord


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vin: Mapped[str] = mapped_column(String(17), unique=True, index=True, nullable=False)
    plate_number: Mapped[str] = mapped_column(String(15), unique=True, index=True, nullable=False)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    operator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    assigned_operator: Mapped["User | None"] = relationship(back_populates="vehicles")
    telemetry_logs: Mapped[list["TelemetryRecord"]] = relationship(
        back_populates="vehicle", cascade="all, delete-orphan"
    )