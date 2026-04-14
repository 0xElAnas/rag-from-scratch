from pydantic import BaseModel

class DocumentRequest(BaseModel):
    filename: str
    content: bytes
    
class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    page_count: int | None = None
    chunk_count: int | None = None