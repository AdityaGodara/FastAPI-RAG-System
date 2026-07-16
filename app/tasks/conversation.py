import asyncio

from app.celery_app import celery
from app.db.database import SessionLocal
from app.conversations.service import ConversationService


@celery.task
def generate_conversation_title(
    conversation_id: str,
    question: str,
    answer: str,
):
    asyncio.run(
        _generate_title(
            conversation_id,
            question,
            answer,
        )
    )


async def _generate_title(
    conversation_id,
    question,
    answer,
):

    async with SessionLocal() as db:

        service = ConversationService(db)

        await service.generate_title(
            conversation_id,
            question,
            answer,
        )