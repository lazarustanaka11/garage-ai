from app.auth.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest, Token, UserCreate


class AuthService:
    """Service responsible for authentication and user registration."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def register(self, user: UserCreate) -> User:
        """Register a new user."""

        existing_user = self.repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("A user with this email already exists.")

        hashed_password = hash_password(user.password)

        return self.repository.create(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
        )

    def login(self, credentials: LoginRequest) -> Token:
        """Authenticate a user and return an access token."""

        user = self.repository.get_by_email(credentials.email)

        if user is None:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        access_token = create_access_token(str(user.id))

        return Token(
            access_token=access_token,
        )
