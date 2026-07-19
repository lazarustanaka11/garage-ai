from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.repositories.repair_job_repository import RepairJobRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.repair_job import (
    RepairJobCreate,
    RepairJobResponse,
    RepairJobUpdate,
)
from app.services.repair_job_service import RepairJobService

router = APIRouter(
    prefix="/api/repair-jobs",
    tags=["Repair Jobs"],
)


def get_repair_job_service(
    db: Session,
) -> RepairJobService:
    """Return a RepairJobService instance."""

    return RepairJobService(
        repair_job_repository=RepairJobRepository(db),
        vehicle_repository=VehicleRepository(db),
    )


@router.post(
    "",
    response_model=RepairJobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_repair_job(
    repair_job: RepairJobCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RepairJobResponse:
    """Create a repair job."""

    service = get_repair_job_service(db)

    try:
        return service.create(repair_job)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[RepairJobResponse],
)
def get_repair_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[RepairJobResponse]:
    """Return all repair jobs."""

    service = get_repair_job_service(db)

    return service.get_all()


@router.get(
    "/{repair_job_id}",
    response_model=RepairJobResponse,
)
def get_repair_job(
    repair_job_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RepairJobResponse:
    """Return a repair job."""

    service = get_repair_job_service(db)

    try:
        return service.get_by_id(repair_job_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.put(
    "/{repair_job_id}",
    response_model=RepairJobResponse,
)
def update_repair_job(
    repair_job_id: UUID,
    repair_job: RepairJobUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RepairJobResponse:
    """Update a repair job."""

    service = get_repair_job_service(db)

    try:
        return service.update(
            repair_job_id,
            repair_job,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Repair job not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


@router.delete(
    "/{repair_job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_repair_job(
    repair_job_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> None:
    """Delete a repair job."""

    service = get_repair_job_service(db)

    try:
        service.delete(repair_job_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
