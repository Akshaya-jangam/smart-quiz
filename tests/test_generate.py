import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import QuizResponse

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version_info():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "generator_mode" in data
    assert "supported_difficulties" in data
    assert "supported_types" in data

def test_generate_quiz():
    payload = {
        "goal": "CAT",
        "num_questions": 5,
        "difficulty": "intermediate"
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "quiz_id" in data
    assert data["goal"] == "CAT"
    assert len(data["questions"]) == 5
    
    for question in data["questions"]:
        assert question["type"] in ["mcq", "short_answer"]
        assert question["difficulty"] == "intermediate"
        assert "answer" in question
        if question["type"] == "mcq":
            assert len(question["options"]) == 4

def test_generate_with_invalid_difficulty():
    payload = {
        "goal": "CAT",
        "num_questions": 5,
        "difficulty": "expert"  # Not in supported difficulties
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422  # Validation error