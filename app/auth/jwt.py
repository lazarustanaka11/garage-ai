from datetime import datetime, timedelta, timezone


from app.core.config import settings
from uuid import UUID

from jose import JWTError, jwt


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    
def decode_access_token(token: str) -> UUID:
    """Decode a JWT and return the user ID."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        subject = payload.get("sub")

        if subject is None:
            raise ValueError("Token is missing subject.")

        return UUID(subject)

    except (JWTError, ValueError):
        raise ValueError("Invalid or expired token.")
