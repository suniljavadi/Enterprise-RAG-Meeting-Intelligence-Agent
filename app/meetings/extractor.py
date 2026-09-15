import re
from datetime import datetime

def extract_meeting(text: str, title: str = "Meeting") -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    def collect(label: str) -> list[str]:
        return [line.split(":", 1)[1].strip() if ":" in line else line for line in lines if label in line.lower()]
    decisions = collect("decision")
    risks = collect("risk")
    dependencies = collect("depend")
    questions = collect("question")
    actions = []
    for line in lines:
        match = re.search(r"(?:action|todo)\s*:\s*(.+?)(?:\s+owner\s*:\s*(.+?))?(?:\s+deadline\s*:\s*(\S+))?$", line, re.I)
        if match:
            actions.append({"action": match.group(1).strip(), "owner": (match.group(2) or "Unassigned").strip(), "deadline": match.group(3), "status": "OPEN"})
    summary = " ".join(lines[:3])[:1000] or "No summary available."
    return {"title": title, "meeting_date": datetime.utcnow(), "summary": summary, "decisions": decisions, "actions": actions, "risks": risks, "dependencies": dependencies, "questions": questions}
