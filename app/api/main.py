import logging
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.agents.agent import run_agent
from app.database.models import ActionItem, Document, Meeting
from app.database.session import get_db, init_db
from app.ingestion.service import ingest_document
from app.rag.service import answer_query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
app = FastAPI(title="Enterprise RAG & Meeting Intelligence Agent", version="1.0.0", lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    tenant_id: str = "public"
    agent: bool = True

@app.get("/health")
def health():
    return {"status": "ok", "service": "enterprise-rag-agent"}

@app.post("/api/v1/documents/upload")
async def upload(request: Request, filename: str = Query("upload.txt"), x_filename: str | None = Header(None), db: Session = Depends(get_db)):
    try:
        document = ingest_document(db, x_filename or filename, await request.body())
        return {"document_id": document.document_id, "filename": document.filename, "status": document.status}
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

@app.post("/api/v1/documents/index")
def index_documents(db: Session = Depends(get_db)):
    count = db.query(Document).filter_by(status="indexed").count()
    return {"indexed_documents": count, "status": "complete"}

@app.post("/api/v1/query")
def query(request: QueryRequest, db: Session = Depends(get_db)):
    return run_agent(db, request.question) if request.agent else answer_query(db, request.question, request.tenant_id)

@app.get("/api/v1/documents/{document_id}")
def document(document_id: str, db: Session = Depends(get_db)):
    item = db.query(Document).filter_by(document_id=document_id).first()
    if not item:
        raise HTTPException(404, "Document not found")
    return {"document_id": item.document_id, "filename": item.filename, "type": item.document_type, "status": item.status, "chunks": len(item.chunks)}

@app.get("/api/v1/meetings")
def meetings(db: Session = Depends(get_db)):
    return [{"meeting_id": m.meeting_id, "title": m.title, "summary": m.summary, "decisions": m.decisions, "risks": m.risks} for m in db.query(Meeting).all()]

@app.get("/api/v1/action-items")
def action_items(db: Session = Depends(get_db)):
    return [{"action": a.action, "owner": a.owner, "deadline": a.deadline, "status": a.status} for a in db.query(ActionItem).all()]
