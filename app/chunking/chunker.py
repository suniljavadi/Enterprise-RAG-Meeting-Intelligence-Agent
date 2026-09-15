import re
from uuid import uuid4

def clean_text(text: str) -> str:
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()

def chunk_text(text: str, pages: list[dict], max_chars: int = 900, overlap: int = 120) -> list[dict]:
    text = clean_text(text)
    if not text:
        return []
    sections = re.split(r"\n(?=\s*(?:#{1,6}\s+|[A-Z][A-Za-z0-9 /&-]{2,60}:\s*$))", text)
    chunks = []
    for raw in sections:
        raw = raw.strip()
        if not raw:
            continue
        lines = raw.splitlines()
        section = "General"
        if lines and (lines[0].startswith("#") or lines[0].endswith(":")):
            section = lines[0].lstrip("# ").rstrip(":")[:255] or "General"
        start = 0
        while start < len(raw):
            end = min(len(raw), start + max_chars)
            if end < len(raw):
                boundary = max(raw.rfind(". ", start, end), raw.rfind("\n", start, end))
                if boundary > start + max_chars // 2:
                    end = boundary + 1
            part = raw[start:end].strip()
            page = next((p["page"] for p in pages if part[:40] in p.get("text", "")), pages[0]["page"] if pages else 1)
            chunks.append({"chunk_id": str(uuid4()), "text": part, "page": page, "section": section})
            if end >= len(raw):
                break
            start = max(end - overlap, start + 1)
    return chunks
