from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import oauth2_scheme
from app.database.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Return the authenticated user."""

    service = AuthService(UserRepository(db))

    try:
        return service.get_current_user(token)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
