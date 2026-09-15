from sqlalchemy.orm import Session
from app.rag.service import answer_query
from app.retrieval.hybrid import search
from app.database.models import ActionItem, Meeting

def search_documents(db: Session, query: str) -> list[dict]:
    return [{"text": x["chunk"].text, "document": x["document"].filename, "page": x["chunk"].page, "section": x["chunk"].section, "score": x["score"]} for x in search(db, query)]

def retrieve_document(db: Session, document_id: str):
    from app.database.models import Document
    return db.query(Document).filter_by(document_id=document_id).first()

def search_meetings(db: Session, query: str) -> list[Meeting]:
    return db.query(Meeting).filter(Meeting.summary.ilike(f"%{query}%")).all()

def get_action_items(db: Session, status: str | None = None) -> list[ActionItem]:
    query = db.query(ActionItem)
    return query.filter_by(status=status).all() if status else query.all()

def search_incidents(db: Session, query: str) -> list[dict]:
    return search_documents(db, f"incident {query}")

def compare_documents(db: Session, first_id: str, second_id: str) -> dict:
    first, second = retrieve_document(db, first_id), retrieve_document(db, second_id)
    if not first or not second:
        raise ValueError("Both documents must exist")
    a, b = set(first.content.lower().split()), set(second.content.lower().split())
    return {"common_points": sorted(a & b)[:30], "differences": sorted(a ^ b)[:30], "additions": sorted(b - a)[:30], "removals": sorted(a - b)[:30], "risks": [x for x in sorted(b - a) if x in {"risk", "timeout", "rollback", "failure"}], "important_changes": "Lexical comparison of indexed document content."}

def summarize_document(db: Session, document_id: str) -> dict:
    document = retrieve_document(db, document_id)
    if not document:
        raise ValueError("Document not found")
    return answer_query(db, f"Summarize {document.filename}")
