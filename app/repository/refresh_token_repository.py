from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token