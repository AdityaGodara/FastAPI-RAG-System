from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.documents.router import router as document_router

from contextlib import asynccontextmanager

from app.storage.service import StorageService

app = FastAPI(
    title="FastAPI RAG",
    description="A FastAPI application with RAG (Retrieval-Augmented Generation) capabilities.",
    version="1.0.0",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage = StorageService()
    storage.ensure_bucket_exists()

    yield

app.include_router(auth_router)
app.include_router(document_router)
