from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import ChatResponse, SourceChunk
from app.repository.conversation_repository import ConversationRepository
from app.repository.message_repository import MessageRepository
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.service import LLMService
from app.models.enums import MessageRole
from app.models.message import Message
from app.retrieval.service import RetrievalService
from app.tasks.conversation import generate_conversation_title


class ChatService:

    def __init__(self, db: AsyncSession):
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.retrieval_service = RetrievalService(db)
        self.llm = LLMService()

    async def chat(
        self,
        conversation_id: UUID,
        document_id: UUID,
        question: str,
        user_id: UUID,
    ):

        # -----------------------------
        # Validate Conversation
        # -----------------------------
        conversation = await self.conversation_repo.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden",
            )

        # -----------------------------
        # Save User Message
        # -----------------------------
        await self.message_repo.create(
            Message(
                conversation_id=conversation_id,
                role=MessageRole.USER,
                content=question,
            )
        )

        # -----------------------------
        # Conversation History
        # -----------------------------
        messages = await self.message_repo.get_by_conversation(
            conversation_id=conversation_id,
            limit=10,
        )

        history = [
            {
                "role": message.role.value.lower(),
                "content": message.content,
            }
            for message in messages
        ]

        # -----------------------------
        # Retrieval
        # -----------------------------
        chunks = await self.retrieval_service.retrieve(
            document_id=document_id,
            question=question,
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        # -----------------------------
        # LLM
        # -----------------------------
        answer = await self.llm.generate(
            system_prompt=SYSTEM_PROMPT.format(
                context=context,
            ),
            history=history,
            user_prompt=question,
        )

        # -----------------------------
        # Save Assistant Message
        # -----------------------------
        await self.message_repo.create(
            Message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=answer,
            )
        )

        if not conversation.title_generated:
            generate_conversation_title.delay(
                str(conversation_id)
            )

        # -----------------------------
        # Response
        # -----------------------------
        return ChatResponse(
            answer=answer,
            sources=[
                SourceChunk(
                    chunk_id=chunk.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                )
                for chunk in chunks
            ],
        )