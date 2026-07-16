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

@router.post("/ask", response_model=ChatResponse)
async def chat_test(chat: ChatRequest, 
                    user: User = Depends(get_current_user), 
                    db: AsyncSession = Depends(get_db)):
    service = ChatService(db)

    answer = await service.chat(
        document_id=chat.document_id,
        question=chat.question
    )

    return answer