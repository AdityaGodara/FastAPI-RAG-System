from app.db.base_class import Base

# Import every model here
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.document import Document
from app.models.injestion_job import IngestionJob
from app.models.document_chunk import DocumentChunk