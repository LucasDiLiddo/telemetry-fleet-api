from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TelemetryCreate(BaseModel):
    vehicle_id: int
    speed: float = Field(..., ge=0.0, le=400.0, description="Velocidad en km/h")
    fuel_level: float = Field(..., ge=0.0, le=100.0, description="Nivel de combustible/batería en %")
    engine_temp: float = Field(..., ge=-40.0, le=180.0, description="Temperatura de motor en °C")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TelemetryResponse(TelemetryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Schema analítico: estadísticas agregadas de una flota/vehículo
class TelemetryStats(BaseModel):
    vehicle_id: int
    total_records: int
    avg_speed: float
    max_speed: float
    current_fuel: float
    avg_engine_temp: float
    last_reported_at: datetime | None = None