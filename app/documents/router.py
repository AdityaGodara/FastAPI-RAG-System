from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.documents.schemas import DocumentResponse, DocFetchResponse
from app.documents.service import DocumentService
from app.models.user import User

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)

    return await service.upload_document(
        file=file,
        user_id=current_user.id,
    )

@router.get("", response_model=list[DocFetchResponse])
async def get_all_documents(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = DocumentService(db)

    result = await service.list_documents(user.id)

    return result

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from uuid import UUID
    service = DocumentService(db)
    await service.delete_document(UUID(document_id), user.id)
    return {"message": "Document deleted"}