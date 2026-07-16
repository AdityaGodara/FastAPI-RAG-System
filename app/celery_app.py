from celery import Celery

from app.core.config import settings

celery = Celery(
    "rag-worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.ingestion"],
)

import app.db.base

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    imports=(
        "app.tasks.ingestion",
        "app.tasks.conversation",
    )
)

# celery.autodiscover_tasks(["app.tasks"])