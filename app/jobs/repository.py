from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.injestion_job import IngestionJob
from app.models.enums import JobStatus


class IngestionJobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, job: IngestionJob) -> IngestionJob:
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def get_by_id(self, job_id: UUID) -> IngestionJob | None:
        result = await self.db.execute(
            select(IngestionJob).where(IngestionJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_by_document_id(
        self,
        document_id: UUID,
    ) -> IngestionJob | None:
        result = await self.db.execute(
            select(IngestionJob).where(
                IngestionJob.document_id == document_id
            )
        )
        return result.scalar_one_or_none()

    async def update(self, job: IngestionJob) -> IngestionJob:
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def delete(self, job: IngestionJob) -> None:
        await self.db.delete(job)
        await self.db.commit()

    async def set_status(
        self,
        job: IngestionJob,
        status: JobStatus,
    ) -> IngestionJob:
        job.status = status
        await self.db.commit()
        await self.db.refresh(job)
        return job