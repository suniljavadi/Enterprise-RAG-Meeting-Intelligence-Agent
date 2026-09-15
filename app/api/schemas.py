from pydantic import BaseModel

class Citation(BaseModel):
    document: str
    page: int | None
    section: str
    chunk_id: str

class QueryResponse(BaseModel):
    answer: str
    evidence: list[dict]
    citations: list[Citation]
    confidence: float
