from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:
    """Repository for vehicle database operations."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with database session."""
        self.db = db

    def create(
        self,
        *,
        customer_id: UUID,
        make: str,
        model: str,
        year: int,
        vin: str,
        license_plate: str,
        mileage: int,
        color: str,
        last_service_date: date | None,
    ) -> Vehicle:
        """Create a new vehicle."""

        vehicle = Vehicle(
            customer_id=customer_id,
            make=make,
            model=model,
            year=year,
            vin=vin,
            license_plate=license_plate,
            mileage=mileage,
            color=color,
            last_service_date=last_service_date,
        )

        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle

    def get_all(self) -> list[Vehicle]:
        """Return all vehicles."""

        return list(self.db.scalars(select(Vehicle)).all())

    def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        """Return a vehicle by its ID."""

        return self.db.scalar(
            select(Vehicle).where(
                Vehicle.id == vehicle_id
            )
        )

    def get_by_customer(self, customer_id: UUID) -> list[Vehicle]:
        """Return all vehicles belonging to a customer."""

        return list(
            self.db.scalars(
                select(Vehicle).where(
                    Vehicle.customer_id == customer_id
                )
            ).all()
        )

    def get_by_vin(self, vin: str) -> Vehicle | None:
        """Return a vehicle by VIN."""

        return self.db.scalar(
            select(Vehicle).where(
                Vehicle.vin == vin
            )
        )

    def get_by_license_plate(
        self,
        license_plate: str,
    ) -> Vehicle | None:
        """Return a vehicle by license plate."""

        return self.db.scalar(
            select(Vehicle).where(
                Vehicle.license_plate == license_plate
            )
        )

    def update(
        self,
        vehicle: Vehicle,
        *,
        customer_id: UUID,
        make: str,
        model: str,
        year: int,
        vin: str,
        license_plate: str,
        mileage: int,
        color: str,
        last_service_date: date | None,
    ) -> Vehicle:
        """Update an existing vehicle."""

        vehicle.customer_id = customer_id
        vehicle.make = make
        vehicle.model = model
        vehicle.year = year
        vehicle.vin = vin
        vehicle.license_plate = license_plate
        vehicle.mileage = mileage
        vehicle.color = color
        vehicle.last_service_date = last_service_date

        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        """Delete a vehicle."""

        self.db.delete(vehicle)
        self.db.commit()
