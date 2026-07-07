from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.db.database import get_db
from app.schemas.auth import SignupRequest, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
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