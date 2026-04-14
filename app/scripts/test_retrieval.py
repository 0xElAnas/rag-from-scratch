from app.db.session import SessionLocal
from app.services import embedder
from app.services.embedder import Embedder
from app.services.retrieval_service import RetrievalService
from app.services.vector_store import VectorStore

def main():
    db = SessionLocal()
    
    try:
        document_id = "102a1da6-c000-4e95-8cca-37d44ce061b1"
        query = "How many vacation days do employees get?"
        
        retrieval_service = RetrievalService(
            embedder=Embedder(),
            vector_store=VectorStore()
        )

        results = retrieval_service.retrieve(
            db=db,
            question=query,
            document_id=document_id,
            top_k=5
        )   
        
        print("Top similar chunks:")
        for chunk in results:
            print(f"Chunk ID: {chunk.id}, Page: {chunk.page_number}, Text: {chunk.text[:100]}...")
            
    finally:
        db.close()
    
if __name__ == "__main__":
    main()