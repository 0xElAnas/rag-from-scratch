from sqlalchemy import select
from app.db.models import Chunk

class VectorStore:
    def similarity_search(
        self,
        db,
        *,
        query_embedding: list[float],
        document_id: str,
        top_k: int = 5,
    ) -> list[Chunk]:
        """
        Return the top-k most similar chunks for a query embedding
        within a single document.

        Assumes Chunk.embedding is a pgvector-enabled column that
        supports cosine_distance(...).
        """
        if not query_embedding:
            raise ValueError("query_embedding must not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        stmt = (
            select(Chunk)
            .where(Chunk.document_id == document_id)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )

        results = db.scalars(stmt).all()
        return list(results)