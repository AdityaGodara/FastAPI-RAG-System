from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.documents.router import router as document_router
from app.chat.router import router as chat_router
from app.conversations.router import router as conversation_router
from app.websockets.router import router as websocket_router

from contextlib import asynccontextmanager

from app.storage.service import StorageService
from app.core.config import settings

app = FastAPI(
    title="FastAPI RAG",
    description="A FastAPI application with RAG (Retrieval-Augmented Generation) capabilities.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage = StorageService()
    storage.ensure_bucket_exists()

    yield

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(
    websocket_router,
    prefix="/ws",
)
