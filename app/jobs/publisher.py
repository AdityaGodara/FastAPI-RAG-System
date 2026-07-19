import json
from redis.asyncio import Redis

from app.core.config import settings


class JobPublisher:

    async def publish(
        self,
        job_id: str,
        status: str,
        progress: int | None = None,
        error: str | None = None,
    ):
        redis = Redis.from_url(settings.redis_url)

        try:
            await redis.publish(
                f"job:{job_id}",
                json.dumps(
                    {
                        "job_id": job_id,
                        "status": status,
                        "progress": progress,
                        "error": error,
                    }
                ),
            )
        finally:
            await redis.aclose()


publisher = JobPublisher()