from sqlalchemy.orm import Session
from app.rag.service import answer_query
from app.tools.registry import get_action_items, search_documents, search_incidents, search_meetings

def run_agent(db: Session, question: str) -> dict:
    lowered = question.lower()
    if "action" in lowered or "assigned" in lowered:
        return {"tool": "get_action_items", "items": [a.action for a in get_action_items(db)]} | answer_query(db, question)
    if "incident" in lowered:
        return {"tool": "search_incidents"} | answer_query(db, question)
    if "meeting" in lowered or "decision" in lowered or "risk" in lowered:
        return {"tool": "search_meetings", "meetings": [m.title for m in search_meetings(db, question)]} | answer_query(db, question)
    return {"tool": "search_documents"} | answer_query(db, question)
