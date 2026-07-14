from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.chat_repository import RetrievalRepository
from app.embeddings.service import EmbeddingService

from app.llm.service import LLMService
from app.llm.prompts import SYSTEM_PROMPT

from uuid import UUID

class ChatService:

    def __init__(self, db: AsyncSession):
        self.repo = RetrievalRepository(db)
        self.embedding_service = EmbeddingService()
        self.llm = LLMService()


    async def chat(
        self,
        document_id: UUID,
        question: str,
    ):
        query_embedding = await self.embedding_service.embed(question)

        chunks = await self.repo.similarity_search(
            document_id=document_id,
            query_embedding=query_embedding,
            limit=5,
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        system_prompt = SYSTEM_PROMPT.format(context=context)
        answer = await self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=question,
        )

        return answer