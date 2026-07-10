from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document

from sqlalchemy import select

class DocumentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, document: Document) -> Document:
        self.db.add(document)
        return document
    
    async def get_by_id(self, doc_id: UUID) -> Document:
        result = await self.db.execute(
            select(Document).where(Document.id == doc_id)
        )

        return result.scalar_one_or_none()
    
    async def get_by_user(self, user_id: UUID) -> list[Document]:
        result = await self.db.execute(
            select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        )

        return list(result.scalars().all())
    
    async def delete_doc(self, document: Document) -> None:
        await self.db.delete(document)
        await self.db.commit()

    async def update_doc(self, document: Document) -> Document:
        await self.db.commit()
        await self.db.refresh(document)
        return document