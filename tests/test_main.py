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

def test_list_prompts_returns_empty_list() -> None:
    response = client.get("/prompts")

    assert response.status_code == 200
    assert response.json() == []


def test_list_prompts() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Code Review",
            "content": "Review this code for correctness.",
            "tags": ["python"],
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Summarize",
            "content": "Summarize the following text.",
            "tags": ["writing"],
        },
    )

    response = client.get("/prompts")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Code Review"
    assert data[1]["id"] == 2
    assert data[1]["title"] == "Summarize"

def test_get_prompt_by_id() -> None:
    created_response = client.post(
        "/prompts",
        json={
            "title": "Code Review",
            "content": "Review this code for correctness.",
            "tags": ["python", "review"],
        },
    )
    prompt_id = created_response.json()["id"]

    response = client.get(f"/prompts/{prompt_id}")

    assert response.status_code == 200
    assert response.json() == created_response.json()

def test_get_prompt_by_id_returns_not_found() -> None:
    response = client.get("/prompts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

def test_update_prompt() -> None:
    created_response = client.post(
        "/prompts",
        json={
            "title": "Code Review",
            "content": "Review this code for correctness.",
            "tags": ["python", "review"],
        },
    )
    created_prompt = created_response.json()
    prompt_id = created_prompt["id"]

    response = client.put(
        f"/prompts/{prompt_id}",
        json={
            "title": "Python Code Review",
        },
    )

    assert response.status_code == 200

    updated_prompt = response.json()

    assert updated_prompt["id"] == prompt_id
    assert updated_prompt["title"] == "Python Code Review"
    assert updated_prompt["content"] == created_prompt["content"]
    assert updated_prompt["tags"] == created_prompt["tags"]
    assert updated_prompt["created_at"] == created_prompt["created_at"]
    assert datetime.fromisoformat(
        updated_prompt["updated_at"]
    ) >= datetime.fromisoformat(created_prompt["updated_at"])

def test_update_prompt_returns_not_found() -> None:
    response = client.put(
        "/prompts/999",
        json={
            "title": "Updated title",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

def test_delete_prompt() -> None:
    created_response = client.post(
        "/prompts",
        json={
            "title": "Code Review",
            "content": "Review this code for correctness.",
            "tags": ["python", "review"],
        },
    )
    prompt_id = created_response.json()["id"]

    response = client.delete(f"/prompts/{prompt_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/prompts/{prompt_id}")

    assert get_response.status_code == 404

def test_delete_prompt_returns_not_found() -> None:
    response = client.delete("/prompts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

