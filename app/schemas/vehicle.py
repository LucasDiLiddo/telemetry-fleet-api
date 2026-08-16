from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class VehicleBase(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="Vehicle Identification Number (17 chars)")
    plate_number: str = Field(..., min_length=3, max_length=15)
    brand: str = Field(..., max_length=50)
    model_name: str = Field(..., max_length=50)
    status: str = Field(default="active", pattern="^(active|maintenance|retired)$")
    operator_id: int | None = None


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    plate_number: str | None = None
    brand: str | None = None
    model_name: str | None = None
    status: str | None = Field(default=None, pattern="^(active|maintenance|retired)$")
    operator_id: int | None = None


class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)