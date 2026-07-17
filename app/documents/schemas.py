from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import DocumentStatus, MediaType, JobStatus

class DocumentResponse(BaseModel):
    id: UUID
    job_id: UUID
    original_filename: str
    media_type: MediaType
    status: DocumentStatus
    job_status: JobStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DocFetchResponse(BaseModel):
    id: UUID
    filename: str
    media_type: str
    size: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes":True,
    }