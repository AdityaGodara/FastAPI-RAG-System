from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.auth import SignupRequest

from fastapi import HTTPException


class AuthService:

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def signup(self, signup_request: SignupRequest) -> User:
        # Check if the email or username already exists
        existing_user_by_email = await self.user_repo.get_by_email(signup_request.email)
        if existing_user_by_email:
            raise HTTPException(status_code=409, detail="Email already exists")

        existing_user_by_username = await self.user_repo.get_by_username(signup_request.username)
        if existing_user_by_username:
            raise HTTPException(status_code=409, detail="Username already exists")

        # Hash the password
        hashed_password = hash_password(signup_request.password)

        # Create a new user instance
        new_user = User(
            username=signup_request.username,
            email=signup_request.email,
            password_hash=hashed_password,
            is_active=True,
            is_verified=False
        )

        # Save the new user to the database
        created_user = await self.user_repo.create(new_user)

        return created_user