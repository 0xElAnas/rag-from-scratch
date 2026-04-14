from app.services.pdf_parser import PDFParser
from app.services.chunker import TextChunker

parser = PDFParser()
pages = parser.parse("./data/Sample_Employee_Handbook.pdf")

chunker = TextChunker(chunk_size=800, chunk_overlap=100)
chunks = chunker.chunk_pages(pages)

print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(chunks)}")

for chunk in chunks[:10]:
    print(chunk["chunk_index"], chunk["page_number"], chunk["text"])
    print("-" * 40)