from uuid import UUID

from app.embeddings.service import EmbeddingService
from app.repository.chat_repository import RetrievalRepository


class RetrievalService:

    def __init__(self, db):
        self.embedding = EmbeddingService()
        self.repository = RetrievalRepository(db)

    async def retrieve(
        self,
        document_id: UUID,
        question: str,
        limit: int = 5,
    ):
        query_embedding = await self.embedding.embed(question)

        chunks = await self.repository.similarity_search(
            document_id=document_id,
            query_embedding=query_embedding,
            limit=limit,
        )

        return chunks