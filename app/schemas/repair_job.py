from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.repair_job import RepairStatus


class RepairJobCreate(BaseModel):
    """Schema for creating a repair job."""

    vehicle_id: UUID
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    mileage: int = Field(ge=0)


class RepairJobUpdate(BaseModel):
    """Schema for updating a repair job."""

    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    mileage: int = Field(ge=0)
    technician_notes: str | None = None
    ai_diagnosis: str | None = None
    status: RepairStatus


class RepairJobResponse(BaseModel):
    """Schema for returning a repair job."""

    id: UUID
    vehicle_id: UUID
    title: str
    description: str
    mileage: int
    technician_notes: str | None
    ai_diagnosis: str | None
    status: RepairStatus
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
