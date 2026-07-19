from datetime import UTC, datetime
from uuid import UUID

from app.models.repair_job import RepairJob, RepairStatus
from app.repositories.repair_job_repository import RepairJobRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.repair_job import (
    RepairJobCreate,
    RepairJobUpdate,
)
from app.ai.openai_service import OpenAIService


class RepairJobService:
    """Service for repair job business logic."""

    def __init__(
        self,
        repair_job_repository: RepairJobRepository,
        vehicle_repository: VehicleRepository,
    ) -> None:
        """Initialize service."""

        self.repair_job_repository = repair_job_repository
        self.vehicle_repository = vehicle_repository

    def create(
        self,
        repair_job: RepairJobCreate,
    ) -> RepairJob:
        """Create a repair job."""

        vehicle = self.vehicle_repository.get_by_id(
            repair_job.vehicle_id
        )

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        return self.repair_job_repository.create(
            vehicle_id=repair_job.vehicle_id,
            title=repair_job.title,
            description=repair_job.description,
            mileage=repair_job.mileage,
        )

    def get_all(self) -> list[RepairJob]:
        """Return all repair jobs."""

        return self.repair_job_repository.get_all()

    def get_by_id(
        self,
        repair_job_id: UUID,
    ) -> RepairJob:
        """Return a repair job."""

        repair_job = self.repair_job_repository.get_by_id(
            repair_job_id
        )

        if repair_job is None:
            raise ValueError("Repair job not found.")

        return repair_job

    def update(
        self,
        repair_job_id: UUID,
        repair_job_data: RepairJobUpdate,
    ) -> RepairJob:
        """Update a repair job."""

        repair_job = self.repair_job_repository.get_by_id(
            repair_job_id
        )

        if repair_job is None:
            raise ValueError("Repair job not found.")

        #
        # Business workflow
        #

        if (
            repair_job.status == RepairStatus.COMPLETED
            and repair_job_data.status == RepairStatus.COMPLETED
        ):
            raise ValueError(
                "Repair job is already completed."
            )

        completed_at = repair_job.completed_at

        if (
            repair_job.status != RepairStatus.COMPLETED
            and repair_job_data.status == RepairStatus.COMPLETED
        ):
            completed_at = datetime.now(UTC)

        repair_job.completed_at = completed_at

        return self.repair_job_repository.update(
            repair_job,
            title=repair_job_data.title,
            description=repair_job_data.description,
            mileage=repair_job_data.mileage,
            technician_notes=repair_job_data.technician_notes,
            ai_diagnosis=repair_job_data.ai_diagnosis,
            status=repair_job_data.status,
        )

    def generate_ai_diagnosis(
        self,
        repair_job_id: UUID,
    ) -> RepairJob:
        """Generate an AI diagnosis for a repair job."""

        repair_job = self.repair_job_repository.get_by_id(
            repair_job_id
        )

        if repair_job is None:
            raise ValueError("Repair job not found.")

        vehicle = repair_job.vehicle

        ai_service = OpenAIService()

        diagnosis = ai_service.diagnose(
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            mileage=repair_job.mileage,
            title=repair_job.title,
            description=repair_job.description,
        )

        return self.repair_job_repository.update(
            repair_job,
            title=repair_job.title,
            description=repair_job.description,
            mileage=repair_job.mileage,
            technician_notes=repair_job.technician_notes,
            ai_diagnosis=diagnosis,
            status=repair_job.status,
        )

    def delete(
        self,
        repair_job_id: UUID,
    ) -> None:
        """Delete a repair job."""

        repair_job = self.repair_job_repository.get_by_id(
            repair_job_id
        )

        if repair_job is None:
            raise ValueError("Repair job not found.")

        self.repair_job_repository.delete(repair_job)
