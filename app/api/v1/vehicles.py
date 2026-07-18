from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.repositories.customer_repository import CustomerRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)
from app.services.vehicle_service import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)


def get_vehicle_service(db: Session) -> VehicleService:
    """Return a VehicleService instance."""

    return VehicleService(
        vehicle_repository=VehicleRepository(db),
        customer_repository=CustomerRepository(db),
    )


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> VehicleResponse:
    """Create a vehicle."""

    service = get_vehicle_service(db)

    try:
        return service.create(vehicle)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[VehicleResponse],
)
def get_vehicles(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[VehicleResponse]:
    """Return all vehicles."""

    service = get_vehicle_service(db)

    return service.get_all()


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> VehicleResponse:
    """Return a vehicle."""

    service = get_vehicle_service(db)

    try:
        return service.get_by_id(vehicle_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle(
    vehicle_id: UUID,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> VehicleResponse:
    """Update a vehicle."""

    service = get_vehicle_service(db)

    try:
        return service.update(
            vehicle_id,
            vehicle,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Vehicle not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> None:
    """Delete a vehicle."""

    service = get_vehicle_service(db)

    try:
        service.delete(vehicle_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
