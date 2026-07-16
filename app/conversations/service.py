from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.conversation_repository import ConversationRepository
from app.repository.message_repository import MessageRepository
from app.schemas.conversation import (
    ConversationCreateResponse,
    ConversationResponse,
)
from app.models.conversation import Conversation
from app.schemas.message import MessageResponse
from app.llm.service import LLMService


class ConversationService:

    def __init__(self, db: AsyncSession):
        self.repo = ConversationRepository(db)
        self.msg_repo = MessageRepository(db)
        self.llm = LLMService()

    async def create(
        self,
        user_id: UUID,
    ) -> ConversationCreateResponse:

        conversation = Conversation(
            user_id=user_id,
            title="New Chat",
        )

        conversation = await self.repo.create(conversation)

        return ConversationCreateResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
        )

    async def list_user_conversations(
        self,
        user_id: UUID,
    ) -> list[ConversationResponse]:

        conversations = await self.repo.get_by_user(user_id)

        return [
            ConversationResponse(
                id=conversation.id,
                title=conversation.title,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
            )
            for conversation in conversations
        ]
    
    async def get_messages(
            self,
            conversation_id: UUID,
            user_id: UUID
    ) -> list[MessageResponse]:
        
        conversation = await self.repo.get_by_id(conversation_id=conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        
        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )
        
        messages = await self.msg_repo.get_by_conversation(conversation_id)

        return [
            MessageResponse(
                id = message.id,
                role = message.role,
                content = message.content,
                created_at = message.created_at
            )
            for message in messages
        ]

    async def generate_title(
        self,
        conversation_id: UUID,
        question:str,
        answer:str
    ):
        conversation = await self.repo.get_by_id(
            conversation_id
        )
        if conversation is None:
            return
        
        if conversation.title != "New Chat":
            return
        
        title = await self.llm.generate_title(
            question,
            answer
        )

        await self.repo.update_title(
            conversation=conversation,
            title=title
        )