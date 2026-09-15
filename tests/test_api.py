import os
os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"
from fastapi.testclient import TestClient
from app.api.main import app
from app.database.session import init_db

init_db()
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200 and response.json()["status"] == "ok"

def test_query_without_context():
    response = client.post("/api/v1/query", json={"question": "What is not known?"})
    assert response.status_code == 200
    assert "answer" in response.json()
