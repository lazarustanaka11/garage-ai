from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Vehicle(Base):
    """Vehicle model."""

    __tablename__ = "vehicles"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    customer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    make: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    year: Mapped[int] = mapped_column(
        nullable=False,
    )

    vin: Mapped[str] = mapped_column(
        String(17),
        unique=True,
        nullable=False,
    )

    license_plate: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    mileage: Mapped[int] = mapped_column(
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    last_service_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    customer: Mapped["Customer"] = relationship(
        back_populates="vehicles",
    )
    repair_jobs: Mapped[list["RepairJob"]] = relationship(
    back_populates="vehicle",
)
