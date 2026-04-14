from fastapi import FastAPI

from app.api.routes import health, documents, chat

app = FastAPI(title="RAG Backend")

app.include_router(health.router)
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])