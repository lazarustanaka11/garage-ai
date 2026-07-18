from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    """Repository responsible for customer database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        name: str,
        email: str,
        phone: str,
    ) -> Customer:
        """Create and persist a new customer."""

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
        )

        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def get_all(self) -> list[Customer]:
        """Return all customers."""

        statement = select(Customer)
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:
        """Return a customer by ID."""

        statement = select(Customer).where(
            Customer.id == customer_id,
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> Customer | None:
        """Return a customer by email."""

        statement = select(Customer).where(
            Customer.email == email,
        )

        return self.db.scalar(statement)

    def update(
        self,
        customer: Customer,
        *,
        name: str,
        email: str,
        phone: str,
    ) -> Customer:
        """Update an existing customer."""

        customer.name = name
        customer.email = email
        customer.phone = phone

        self.db.commit()
        self.db.refresh(customer)

        return customer

    def delete(
        self,
        customer: Customer,
    ) -> None:
        """Delete a customer."""

        self.db.delete(customer)
        self.db.commit()
