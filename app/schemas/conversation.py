from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationCreateResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime