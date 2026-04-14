from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Document
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService
from app.services.prompt_builder import PromptBuilder
from app.services.generation_service import GenerationService


router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    document = db.get(Document, request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    if document.status != "ready":
        raise HTTPException(status_code=400, detail="Document is not ready for querying.")

    embedder = Embedder()
    vector_store = VectorStore()
    retrieval_service = RetrievalService(embedder, vector_store)
    prompt_builder = PromptBuilder()
    generation_service = GenerationService()

    try:
        chunks = retrieval_service.retrieve(
            db=db,
            question=request.question,
            document_id=request.document_id,
            top_k=5,
        )

        prompt = prompt_builder.build_answer_prompt(
            question=request.question,
            chunks=chunks,
        )

        answer = generation_service.generate_answer(prompt)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat pipeline failed: {str(e)}") from e

    sources = [
        SourceItem(
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            page_number=chunk.page_number,
            snippet=chunk.text[:250],
        )
        for chunk in chunks
    ]

    return ChatResponse(
        answer=answer,
        sources=sources,
    )