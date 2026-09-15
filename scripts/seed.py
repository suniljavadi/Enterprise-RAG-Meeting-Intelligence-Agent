from pathlib import Path
from uuid import uuid4
from app.database.models import ActionItem, Meeting
from app.database.session import SessionLocal, init_db
from app.ingestion.service import ingest_document
from app.meetings.extractor import extract_meeting

ROOT = Path(__file__).parents[1]
def main():
    init_db()
    db = SessionLocal()
    for path in (ROOT / "sample_documents").iterdir():
        if path.is_file():
            try: ingest_document(db, path.name, path.read_bytes(), "synthetic-sample")
            except ValueError as exc: print(f"Skipping {path.name}: {exc}")
    for path in (ROOT / "sample_meetings").iterdir():
        parsed = extract_meeting(path.read_text(encoding="utf-8"), path.stem.replace("_", " ").title())
        meeting = Meeting(meeting_id=str(uuid4()), title=parsed["title"], meeting_date=parsed["meeting_date"], summary=parsed["summary"], decisions=parsed["decisions"], risks=parsed["risks"], dependencies=parsed["dependencies"], questions=parsed["questions"])
        db.add(meeting); db.flush()
        for item in parsed["actions"]: db.add(ActionItem(meeting_id=meeting.meeting_id, **item))
    db.commit(); db.close(); print("Synthetic data seeded.")
if __name__ == "__main__": main()
