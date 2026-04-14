from app.db.session import SessionLocal
from app.services.pdf_parser import PDFParser
from app.services.chunker import TextChunker
from app.services.embedder import Embedder
from app.services.ingestion_service import IngestionService

def main():
    # 1. Create DB session
    db = SessionLocal()

    try: 
        # 2. Instantiate services
        parser = PDFParser()
        chunker = TextChunker(chunk_size=500, chunk_overlap=50)
        embedder = Embedder()

        ingestion_service = IngestionService(parser, chunker, embedder)

        # 3. Run ingestion
        file_path = "./data/Sample_Employee_Handbook.pdf"
        filename = "Sample_Employee_Handbook.pdf"

        document, num_chunks = ingestion_service.ingest_pdf(
            db=db,
            file_path=file_path,
            filename=filename
        )

        print("✅ Ingestion completed")
        print("Document ID:", document.id)
        print("Status:", document.status)
        print("Chunks stored:", num_chunks)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()