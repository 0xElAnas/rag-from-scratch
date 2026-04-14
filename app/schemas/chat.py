from pydantic import BaseModel

class ChatRequest(BaseModel):
    document_id: str
    question: str


class SourceItem(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]