from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.repository import DocumentRepository
from app.jobs.repository import IngestionJobRepository
from app.documents.schemas import DocumentResponse
from app.models.document import Document
from app.models.injestion_job import IngestionJob
from app.models.enums import DocumentStatus, MediaType, JobStatus
from app.storage.service import StorageService


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.repository = DocumentRepository(db)
        self.storage = StorageService()
        self.job_repo = IngestionJobRepository(db)

    def _get_media_type(self, file: UploadFile) -> MediaType:
        content_type = file.content_type

        if content_type == "application/pdf":
            return MediaType.PDF

        if content_type.startswith("image/"):
            return MediaType.IMAGE

        if content_type.startswith("audio/"):
            return MediaType.AUDIO

        if content_type.startswith("video/"):
            return MediaType.VIDEO

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type."
        )

    async def upload_document(
        self,
        file: UploadFile,
        user_id: UUID,
    ) -> DocumentResponse:

        media_type = self._get_media_type(file)

        object_key = await self.storage.upload_file(
            file=file,
            user_id=user_id,
            media_type=media_type.value,
        )

        try:
            document = Document(
                user_id=user_id,
                original_filename=file.filename or "unknown",
                object_key=object_key,
                media_type=media_type,
                status=DocumentStatus.UPLOADED,
                file_size=file.size,
                content_type=file.content_type,
            )

            document = await self.repository.create(document)

            job = IngestionJob(
                document_id=document.id,
                status=JobStatus.PENDING
            )

            job = await self.job_repo.create(job)

            await self.db.commit()

            return DocumentResponse(
                id=document.id,
                job_id=job.id,
                original_filename=document.original_filename,
                media_type=document.media_type,
                status=document.status,
                job_status=job.status,
                created_at=document.created_at,
            )

        except Exception:
            self.storage.delete_file(object_key)
            raise