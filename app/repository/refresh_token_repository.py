from sqlalchemy import select, delete
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
    
    async def get_by_hash(self, hash: str) -> RefreshToken | None:
        token = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == hash
            )
        )
        return token.scalar_one_or_none()
    
    async def revoke_ref_token(self, token: RefreshToken) -> None:
        await self.db.delete(token)
        await self.db.commit()