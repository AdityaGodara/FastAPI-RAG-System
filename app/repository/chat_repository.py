from uuid import UUID

# from pgvector.sqlalchemy import cosine_distance
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_chunk import DocumentChunk


class RetrievalRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def similarity_search(
        self,
        document_id: UUID,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:

        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())