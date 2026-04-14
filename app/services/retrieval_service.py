from app.db.models import Chunk
from sqlalchemy.orm import Session
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore

class RetrievalService:
    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, db: Session, *, question: str, document_id: str, top_k: int = 5) -> list[Chunk]:
        if not question or not question.strip():
            raise ValueError("question must not be empty")

        if not document_id:
            raise ValueError("document_id must be provided")
        
        query_embedding = self.embedder.embed_query(question)
        
        results = self.vector_store.similarity_search(
            db=db,
            query_embedding=query_embedding,
            document_id=document_id,
            top_k=top_k
        )
        
        return results