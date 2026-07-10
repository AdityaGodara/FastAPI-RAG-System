import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import SessionLocal
from app.documents.repository import DocumentRepository
from app.jobs.repository import IngestionJobRepository
from app.storage.service import StorageService
from app.models.enums import JobStatus


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_repo = IngestionJobRepository(db)
        self.doc_repo = DocumentRepository(db)
        self.storage = StorageService()

    async def process(self, job_id: str):
        job = await self.job_repo.get_by_id(job_id)

        if job is None:
            raise ValueError(f"Job {job_id} not found")

        document = await self.doc_repo.get_by_id(job.document_id)

        if document is None:
            raise ValueError("Document not found")

        response = self.storage.download_file(document.object_key)

        try:
            file_bytes = response.read()

            print("=" * 60)
            print(f"Filename   : {document.original_filename}")
            print(f"Media Type : {document.media_type}")
            print(f"Size       : {len(file_bytes)} bytes")
            print("=" * 60)

        finally:
            response.close()
            response.release_conn()