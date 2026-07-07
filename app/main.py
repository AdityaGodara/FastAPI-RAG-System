from fastapi import FastAPI
from app.auth.router import router as auth_router

app = FastAPI(
    title="FastAPI RAG",
    description="A FastAPI application with RAG (Retrieval-Augmented Generation) capabilities.",
    version="1.0.0",
)

app.include_router(auth_router)