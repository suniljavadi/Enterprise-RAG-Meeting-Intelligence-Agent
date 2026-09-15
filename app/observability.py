import logging
import uuid

logger = logging.getLogger("enterprise_rag")
def request_id() -> str:
    return str(uuid.uuid4())
def log_query(query: str, latency_ms: float, citations: int, confidence: float) -> None:
    logger.info("request_id=%s query=%r retrieval_latency_ms=%s citations=%s confidence=%s", request_id(), query, latency_ms, citations, confidence)
