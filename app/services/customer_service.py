from uuid import UUID

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service responsible for customer business logic."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def create(self, customer: CustomerCreate) -> Customer:
        """Create a new customer."""

        existing_customer = self.repository.get_by_email(customer.email)

        if existing_customer:
            raise ValueError("A customer with this email already exists.")

        return self.repository.create(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
        )

    def get_all(self) -> list[Customer]:
        """Return all customers."""

        return self.repository.get_all()

    def get_by_id(self, customer_id: UUID) -> Customer:
        """Return a customer by ID."""

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            raise ValueError("Customer not found.")

        return customer

    def update(
        self,
        customer_id: UUID,
        customer_data: CustomerUpdate,
    ) -> Customer:
        """Update an existing customer."""

        customer = self.get_by_id(customer_id)

        existing_customer = self.repository.get_by_email(customer_data.email)

        if (
            existing_customer
            and existing_customer.id != customer.id
        ):
            raise ValueError("A customer with this email already exists.")

        return self.repository.update(
            customer,
            name=customer_data.name,
            email=customer_data.email,
            phone=customer_data.phone,
        )

    def delete(self, customer_id: UUID) -> None:
        """Delete a customer."""

        customer = self.get_by_id(customer_id)

        self.repository.delete(customer)
