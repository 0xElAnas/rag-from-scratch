from sqlalchemy.orm import Session

from app.db.models import Document, Chunk
from app.services.pdf_parser import PDFParser
from app.services.chunker import TextChunker
from app.services.embedder import Embedder


class IngestionService:
    def __init__(self, parser: PDFParser, chunker: TextChunker, embedder: Embedder):
        self.parser = parser
        self.chunker = chunker
        self.embedder = embedder

    def ingest_pdf(self, db: Session, file_path: str, filename: str) -> tuple[Document, int]:
        document = Document(
            filename=filename,
            storage_path=file_path,
            status="processing",
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        try:
            pages = self.parser.parse(file_path)
            chunks = self.chunker.chunk_pages(pages)

            if not chunks:
                raise ValueError("No chunks were generated from the document.")

            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedder.embed_texts(chunk_texts)

            for chunk, embedding in zip(chunks, embeddings):
                chunk_row = Chunk(
                    document_id=document.id,
                    chunk_index=chunk["chunk_index"],
                    page_number=chunk["page_number"],
                    text=chunk["text"],
                    token_count=chunk["token_count"],
                    embedding=embedding,
                )
                db.add(chunk_row)

            document.page_count = len(pages)
            document.status = "ready"

            db.add(document)
            db.commit()
            db.refresh(document)

            return document, len(chunks)

        except Exception as e:
            db.rollback()
            document.status = "failed"
            db.add(document)
            db.commit()
            db.refresh(document)
            raise e