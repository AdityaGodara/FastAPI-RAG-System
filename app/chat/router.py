from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.schemas.chat import ChatResponse, ChatRequest
from app.models.user import User

from app.chat.service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/test")
async def chat_test(chat: ChatRequest, current_user: User = Depends(get_db), db: AsyncSession = Depends(get_db)):
    service = ChatService(db)

    return await service.retrieve(
        document_id=chat.document_id,
        question=chat.question
    )