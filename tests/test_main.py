from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app, prompts

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_prompts() -> Iterator[None]:
    prompts.clear()

    yield

    prompts.clear()


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Prompt Vault API"}


def test_create_prompt() -> None:
    response = client.post(
        "/prompts",
        json={
            "title": "Code Review",
            "content": "Review this code for correctness.",
            "tags": ["python", "review"],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Code Review"
    assert data["content"] == "Review this code for correctness."
    assert data["tags"] == ["python", "review"]
    assert datetime.fromisoformat(data["created_at"])
    assert datetime.fromisoformat(data["updated_at"])


@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "",
            "content": "Valid content",
            "tags": [],
        },
        {
            "title": "Valid title",
            "content": "",
            "tags": [],
        },
    ],
)
def test_create_prompt_rejects_empty_required_fields(
    payload: dict[str, object],
) -> None:
    response = client.post("/prompts", json=payload)

    assert response.status_code == 422
    assert prompts == []