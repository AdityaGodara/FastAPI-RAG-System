from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC, timedelta

from app.core.config import settings

from app.auth.security import hash_password
from app.models.user import User
from app.repository.user_repository import UserRepository

from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse

from fastapi import HTTPException

from app.auth.jwt import create_access_token, create_refresh_token
from app.auth.security import hash_ref_token, verify_password

from app.models.refresh_token import RefreshToken
from app.repository.refresh_token_repository import RefreshTokenRepository


class AuthService:

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

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
    
    async def login(self, login_request: LoginRequest) -> TokenResponse:

        #Fetch user by email
        user = await self.user_repo.get_by_email(login_request.email)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not verify_password(login_request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        hashed_ref_token = hash_ref_token(refresh_token)

        refresh = RefreshToken(
            user_id=user.id,
            token_hash=hashed_ref_token,
            expires_at=datetime.now(UTC)+timedelta( days=settings.refresh_token_expire_days )
        )

        await self.refresh_repo.create(refresh)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
