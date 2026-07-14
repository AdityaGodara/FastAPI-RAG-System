from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    document_id: UUID
    question: str


class ChatResponse(BaseModel):
    answer: str