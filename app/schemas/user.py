from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema for registering a new user."""

    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    """Public representation of a user."""

    id: UUID
    email: EmailStr
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"
