from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    """Schema for creating a vehicle."""

    customer_id: UUID
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1886, le=2100)
    vin: str = Field(min_length=17, max_length=17)
    license_plate: str = Field(min_length=1, max_length=20)
    mileage: int = Field(ge=0)
    color: str = Field(min_length=1, max_length=30)
    last_service_date: date | None = None


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle."""

    customer_id: UUID
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1886, le=2100)
    vin: str = Field(min_length=17, max_length=17)
    license_plate: str = Field(min_length=1, max_length=20)
    mileage: int = Field(ge=0)
    color: str = Field(min_length=1, max_length=30)
    last_service_date: date | None = None


class VehicleResponse(BaseModel):
    """Schema for returning a vehicle."""

    id: UUID
    customer_id: UUID
    make: str
    model: str
    year: int
    vin: str
    license_plate: str
    mileage: int
    color: str
    last_service_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
