from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import DocumentStatus, MediaType


class DocumentResponse(BaseModel):
    id: UUID
    original_filename: str
    media_type: MediaType
    status: DocumentStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }