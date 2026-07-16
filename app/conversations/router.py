from fastapi import APIRouter, Depends
from app.schemas.conversation import ConversationResponse, ConversationCreateResponse
from app.schemas.message import MessageResponse

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.conversations.service import ConversationService

from uuid import UUID

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"]
)

@router.post("", response_model=ConversationCreateResponse)
async def create_conv(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    service = ConversationService(db)

    return await service.create(
        user_id=user.id
    )

@router.get("", response_model=ConversationResponse)
async def get_conv(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    service = ConversationService(db)

    return await service.list_user_conversations(
        user_id=user.id
    )

@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_msgs(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ConversationService(db)

    return await service.get_messages(
        conversation_id=conversation_id,
        user_id=user.id
    )