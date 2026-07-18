from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository responsible for user database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        """Return a user by ID."""
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        email: str,
        hashed_password: str,
        full_name: str,
    ) -> User:
        """Create and persist a new user."""

        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def get_by_id(self, user_id: UUID) -> User | None:
        """Return a user by ID."""

        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)
