from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import Chunk, Document
from app.embeddings.local import embed, cosine

def search(db: Session, query: str, limit: int = 8, tenant_id: str = "public") -> list[dict]:
    query_tokens = set(query.lower().split())
    qvec = embed(query)
    rows = db.execute(select(Chunk, Document).join(Document).where(Document.tenant_id == tenant_id)).all()
    scored = []
    for chunk, document in rows:
        lexical = len(query_tokens & set(chunk.text.lower().split())) / max(len(query_tokens), 1)
        semantic = cosine(qvec, chunk.embedding or embed(chunk.text))
        score = 0.65 * semantic + 0.35 * lexical
        scored.append({"chunk": chunk, "document": document, "score": round(score, 4), "semantic": semantic, "keyword": lexical})
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]

def rerank(results: list[dict], query: str, limit: int = 5) -> list[dict]:
    terms = set(query.lower().split())
    for item in results:
        title_bonus = 0.05 if any(term in item["document"].filename.lower() for term in terms) else 0
        item["rerank_score"] = round(item["score"] + title_bonus, 4)
    return sorted(results, key=lambda item: item["rerank_score"], reverse=True)[:limit]
