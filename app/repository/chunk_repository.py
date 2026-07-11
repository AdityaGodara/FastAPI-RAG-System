from sqlalchemy.ext.asyncio import AsyncSession

class ChunkRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, chunks):
        self.db.add_all(chunks)
        await self.db.flush()