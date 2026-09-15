from pathlib import Path
import io
import pandas as pd

SUPPORTED = {".pdf", ".docx", ".txt", ".md", ".csv"}

def extract_text(filename: str, data: bytes) -> tuple[str, list[dict]]:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {suffix or 'unknown'}")
    if not data.strip():
        raise ValueError("The document is empty")
    if suffix in {".txt", ".md"}:
        return data.decode("utf-8", errors="replace"), [{"page": 1, "text": data.decode("utf-8", errors="replace")}]
    if suffix == ".csv":
        frame = pd.read_csv(io.BytesIO(data))
        text = frame.to_csv(index=False)
        return text, [{"page": 1, "text": text}]
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
            pages = [{"page": i + 1, "text": (page.extract_text() or "")} for i, page in enumerate(PdfReader(io.BytesIO(data)).pages)]
            text = "\n\n".join(p["text"] for p in pages)
            if not text.strip():
                raise ValueError("The PDF contains no extractable text")
            return text, pages
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(f"Could not read PDF: {exc}") from exc
    try:
        from docx import Document as DocxDocument
        doc = DocxDocument(io.BytesIO(data))
        text = "\n".join(p.text for p in doc.paragraphs)
        if not text.strip():
            raise ValueError("The DOCX contains no text")
        return text, [{"page": 1, "text": text}]
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not read DOCX: {exc}") from exc
