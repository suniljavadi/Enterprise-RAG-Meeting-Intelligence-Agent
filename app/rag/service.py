import time
from sqlalchemy.orm import Session
from app.retrieval.hybrid import rerank, search
from app.security.guards import sanitize_document
from app.rag.llm import generate_grounded_answer

NO_EVIDENCE = "I could not find sufficient evidence in the indexed documents."

def citations(results: list[dict]) -> list[dict]:
    return [{"document": x["document"].filename, "page": x["chunk"].page, "section": x["chunk"].section, "chunk_id": x["chunk"].chunk_id} for x in results]

def answer_query(db: Session, question: str, tenant_id: str = "public") -> dict:
    started = time.perf_counter()
    results = rerank(search(db, question, tenant_id=tenant_id), question)
    useful = [r for r in results if r["rerank_score"] >= 0.12]
    if not useful:
        return {"answer": NO_EVIDENCE, "evidence": [], "citations": [], "confidence": 0.0, "retrieval_latency_ms": round((time.perf_counter() - started) * 1000, 2)}
    evidence = [{"text": sanitize_document(r["chunk"].text), "source": r["document"].filename, "page": r["chunk"].page, "section": r["chunk"].section, "score": r["rerank_score"]} for r in useful]
    answer = generate_grounded_answer(question, evidence) or _mock_grounded_answer(question, evidence)
    confidence = round(min(0.98, max(0.35, sum(r["rerank_score"] for r in useful) / len(useful) * 1.8)), 2)
    return {"answer": answer, "evidence": evidence, "citations": citations(useful), "confidence": confidence, "retrieval_latency_ms": round((time.perf_counter() - started) * 1000, 2)}

def _mock_grounded_answer(question: str, evidence: list[dict]) -> str:
    q = question.lower()
    if "action item" in q or "assigned" in q:
        lines = [e["text"] for e in evidence if "action" in e["text"].lower() or "owner" in e["text"].lower()]
        return "Relevant assigned work found in the evidence:\n- " + "\n- ".join(lines[:3]) if lines else evidence[0]["text"]
    if "decision" in q:
        lines = [e["text"] for e in evidence if "decision" in e["text"].lower()]
        return "The indexed meeting evidence records:\n- " + "\n- ".join(lines[:3]) if lines else evidence[0]["text"]
    return "Based on the indexed evidence:\n\n" + "\n\n".join(e["text"] for e in evidence[:3])
