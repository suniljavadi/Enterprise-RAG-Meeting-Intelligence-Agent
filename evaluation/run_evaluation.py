import json
from pathlib import Path
from app.database.session import SessionLocal, init_db
from app.rag.service import answer_query

def main():
    init_db(); db = SessionLocal(); rows = json.loads((Path(__file__).parent / "questions.json").read_text())
    results=[]
    for row in rows:
        result = answer_query(db, row["question"])
        text = (result["answer"] + " " + " ".join(c["document"] for c in result["citations"])).lower()
        hit = row["expected"].lower() in text or (row["type"] == "missing" and result["confidence"] == 0)
        results.append({"id": row["id"], "grounded": hit, "confidence": result["confidence"], "citations": len(result["citations"])})
    summary = {"questions": len(results), "grounded_rate": round(sum(x["grounded"] for x in results)/len(results), 3), "citation_rate": round(sum(bool(x["citations"]) for x in results)/len(results), 3), "results": results}
    Path(__file__).with_name("sample_results.json").write_text(json.dumps(summary, indent=2)); print(json.dumps(summary, indent=2))
if __name__ == "__main__": main()
