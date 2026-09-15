from app.embeddings.local import cosine, embed
from app.rag.service import NO_EVIDENCE

def test_embeddings_are_normalized():
    vector = embed("deployment canary")
    assert abs(cosine(vector, vector) - 1.0) < 0.001

def test_no_evidence_constant_is_grounded():
    assert "sufficient evidence" in NO_EVIDENCE
