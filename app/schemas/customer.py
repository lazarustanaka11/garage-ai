from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    """Schema for creating a customer."""

    name: str
    email: EmailStr
    phone: str


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""

    name: str
    email: EmailStr
    phone: str


class CustomerResponse(BaseModel):
    """Schema returned to clients."""

    id: UUID
    name: str
    email: EmailStr
    phone: str

    model_config = ConfigDict(from_attributes=True)
