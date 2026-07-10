from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.db.database import get_db
from app.schemas.auth import SignupRequest, UserResponse, LoginRequest, TokenResponse, RefreshRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token", response_model=TokenResponse)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    return await service.login(
        LoginRequest(
            email=form_data.username,
            password=form_data.password,
        )
    )

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
)
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)

    return await auth_service.signup(data)

@router.post("/login", response_model=TokenResponse, status_code=200)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)

    return await auth_service.login(data)

@router.post("/refresh", response_model=TokenResponse, status_code=200)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)

    return await auth_service.refresh(data)