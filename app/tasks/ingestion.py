import asyncio

from app.celery_app import celery
from app.db.database import SessionLocal
from app.jobs.service import JobService


@celery.task
def process_document(job_id: str):
    asyncio.run(_process(job_id))


async def _process(job_id: str):
    async with SessionLocal() as db:
        service = JobService(db)
        await service.process(job_id)