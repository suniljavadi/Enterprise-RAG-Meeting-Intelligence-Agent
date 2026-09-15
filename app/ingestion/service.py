from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from app.chunking.chunker import chunk_text
from app.database.models import Chunk, Document
from app.embeddings.local import embed
from app.extraction.extractors import extract_text
from app.security.guards import sanitize_document

def ingest_document(db: Session, filename: str, data: bytes, source: str = "upload") -> Document:
    if db.query(Document).filter_by(filename=filename).first():
        raise ValueError("A document with this filename is already indexed")
    text, pages = extract_text(filename, data)
    text = sanitize_document(text)
    document = Document(document_id=str(uuid4()), filename=filename, document_type=filename.rsplit(".", 1)[-1].lower(), source=source, timestamp=datetime.utcnow(), status="indexed", content=text)
    db.add(document)
    for item in chunk_text(text, pages):
        db.add(Chunk(chunk_id=item["chunk_id"], document_id=document.document_id, text=item["text"], page=item["page"], section=item["section"], embedding=embed(item["text"])))
    db.commit()
    db.refresh(document)
    return document
