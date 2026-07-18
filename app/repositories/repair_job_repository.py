from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repair_job import RepairJob, RepairStatus


class RepairJobRepository:
    """Repository for repair job database operations."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with database session."""
        self.db = db

    def create(
        self,
        *,
        vehicle_id: UUID,
        title: str,
        description: str,
        mileage: int,
    ) -> RepairJob:
        """Create a new repair job."""

        repair_job = RepairJob(
            vehicle_id=vehicle_id,
            title=title,
            description=description,
            mileage=mileage,
        )

        self.db.add(repair_job)
        self.db.commit()
        self.db.refresh(repair_job)

        return repair_job

    def get_all(self) -> list[RepairJob]:
        """Return all repair jobs."""

        return list(
            self.db.scalars(
                select(RepairJob)
            ).all()
        )

    def get_by_id(
        self,
        repair_job_id: UUID,
    ) -> RepairJob | None:
        """Return a repair job by ID."""

        return self.db.scalar(
            select(RepairJob).where(
                RepairJob.id == repair_job_id
            )
        )

    def get_by_vehicle(
        self,
        vehicle_id: UUID,
    ) -> list[RepairJob]:
        """Return all repair jobs for a vehicle."""

        return list(
            self.db.scalars(
                select(RepairJob).where(
                    RepairJob.vehicle_id == vehicle_id
                )
            ).all()
        )

    def update(
        self,
        repair_job: RepairJob,
        *,
        title: str,
        description: str,
        mileage: int,
        technician_notes: str | None,
        ai_diagnosis: str | None,
        status: RepairStatus,
    ) -> RepairJob:
        """Update an existing repair job."""

        repair_job.title = title
        repair_job.description = description
        repair_job.mileage = mileage
        repair_job.technician_notes = technician_notes
        repair_job.ai_diagnosis = ai_diagnosis
        repair_job.status = status

        self.db.commit()
        self.db.refresh(repair_job)

        return repair_job

    def delete(
        self,
        repair_job: RepairJob,
    ) -> None:
        """Delete a repair job."""

        self.db.delete(repair_job)
        self.db.commit()
