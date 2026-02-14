import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_success():
    response = client.post(
        "/query",
        json={"question": "How many students enrolled in Python courses in 2024?"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "generated_sql" in data
    assert "result" in data
    assert "execution_time" in data


def test_stats_endpoint():
    # Call query once
    client.post(
        "/query",
        json={"question": "How many students enrolled in Python courses in 2024?"}
    )

    response = client.get("/stats")

    assert response.status_code == 200
    data = response.json()

    assert "total_queries" in data
    assert data["total_queries"] >= 1