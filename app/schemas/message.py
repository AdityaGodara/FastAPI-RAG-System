from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import MessageRole


class MessageResponse(BaseModel):
    id: UUID
    role: MessageRole
    content: str
    created_at: datetime