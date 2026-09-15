def retrieval_precision(relevant: int, retrieved: int) -> float:
    return relevant / retrieved if retrieved else 0.0

def retrieval_recall(relevant: int, total_relevant: int) -> float:
    return relevant / total_relevant if total_relevant else 0.0

def citation_correctness(correct: int, total: int) -> float:
    return correct / total if total else 0.0
