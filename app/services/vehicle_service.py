from uuid import UUID

from app.models.vehicle import Vehicle
from app.repositories.customer_repository import CustomerRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)


class VehicleService:
    """Service for vehicle business logic."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        customer_repository: CustomerRepository,
    ) -> None:
        self.vehicle_repository = vehicle_repository
        self.customer_repository = customer_repository

    def create(
        self,
        vehicle: VehicleCreate,
    ) -> Vehicle:
        """Create a vehicle."""

        customer = self.customer_repository.get_by_id(
            vehicle.customer_id
        )

        if customer is None:
            raise ValueError("Customer not found.")

        if self.vehicle_repository.get_by_vin(vehicle.vin):
            raise ValueError("VIN already exists.")

        if self.vehicle_repository.get_by_license_plate(
            vehicle.license_plate
        ):
            raise ValueError("License plate already exists.")

        return self.vehicle_repository.create(
            customer_id=vehicle.customer_id,
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            vin=vehicle.vin,
            license_plate=vehicle.license_plate,
            mileage=vehicle.mileage,
            color=vehicle.color,
            last_service_date=vehicle.last_service_date,
        )

    def get_all(self) -> list[Vehicle]:
        """Return all vehicles."""

        return self.vehicle_repository.get_all()

    def get_by_id(
        self,
        vehicle_id: UUID,
    ) -> Vehicle:
        """Return a vehicle by ID."""

        vehicle = self.vehicle_repository.get_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        return vehicle

    def update(
        self,
        vehicle_id: UUID,
        vehicle_data: VehicleUpdate,
    ) -> Vehicle:
        """Update a vehicle."""

        vehicle = self.vehicle_repository.get_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        customer = self.customer_repository.get_by_id(
            vehicle_data.customer_id
        )

        if customer is None:
            raise ValueError("Customer not found.")

        existing_vin = self.vehicle_repository.get_by_vin(
            vehicle_data.vin
        )

        if (
            existing_vin is not None
            and existing_vin.id != vehicle.id
        ):
            raise ValueError("VIN already exists.")

        existing_plate = (
            self.vehicle_repository.get_by_license_plate(
                vehicle_data.license_plate
            )
        )

        if (
            existing_plate is not None
            and existing_plate.id != vehicle.id
        ):
            raise ValueError("License plate already exists.")

        return self.vehicle_repository.update(
            vehicle,
            customer_id=vehicle_data.customer_id,
            make=vehicle_data.make,
            model=vehicle_data.model,
            year=vehicle_data.year,
            vin=vehicle_data.vin,
            license_plate=vehicle_data.license_plate,
            mileage=vehicle_data.mileage,
            color=vehicle_data.color,
            last_service_date=vehicle_data.last_service_date,
        )

    def delete(
        self,
        vehicle_id: UUID,
    ) -> None:
        """Delete a vehicle."""

        vehicle = self.vehicle_repository.get_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        self.vehicle_repository.delete(vehicle)
