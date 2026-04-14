class TextChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(self, pages: list[dict]) -> list[dict]:
        chunks = []
        chunk_index = 0

        for page in pages:
            text = page.get("text", "")
            page_number = page.get("page_number", 0)

            if not text or not text.strip():
                continue

            start = 0

            while start < len(text):
                end = start + self.chunk_size
                chunk_text = text[start:end].strip()

                if chunk_text:
                    chunks.append({
                        "chunk_index": chunk_index,
                        "page_number": page_number,
                        "text": chunk_text,
                        "token_count": len(chunk_text.split())
                    })
                    chunk_index += 1

                if end >= len(text):
                    break

                start += self.chunk_size - self.chunk_overlap

        return chunks