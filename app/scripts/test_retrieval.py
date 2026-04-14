from app.db.session import SessionLocal
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore

def main():
    db = SessionLocal()
    
    embedder = Embedder()
    vectore_store = VectorStore() 

    query = "How many vacation days do employees get?"
    query_emebedding = embedder.embed_query(query)

    document_id = "102a1da6-c000-4e95-8cca-37d44ce061b1"

    results = vectore_store.similarity_search(
        db=db,
        query_embedding=query_emebedding,
        document_id=document_id,
        top_k=5
    )
    
    print("Top similar chunks:")
    for chunk in results:
        print(f"Chunk ID: {chunk.id}, Page: {chunk.page_number}, Text: {chunk.text[:100]}...")
    
if __name__ == "__main__":
    main()