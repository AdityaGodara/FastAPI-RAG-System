from redis.asyncio import Redis

from app.core.config import settings

redis = Redis.from_url(settings.redis_url)


async def subscribe(job_id: str):

    pubsub = redis.pubsub()

    await pubsub.subscribe(f"job:{job_id}")

    try:

        async for message in pubsub.listen():

            if message["type"] == "message":
                yield message["data"].decode()

    finally:

        await pubsub.unsubscribe(f"job:{job_id}")

        await pubsub.close()