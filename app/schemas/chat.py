from uuid import UUID

from pydantic import BaseModel


from typing import Optional

class ChatRequest(BaseModel):
    conversation_id: UUID
    document_id: Optional[UUID] = None
    question: str

class SourceChunk(BaseModel):
    chunk_id: UUID
    chunk_index: int
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]