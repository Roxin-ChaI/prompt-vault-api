from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas import PromptCreate, PromptResponse, PromptUpdate


def test_create_prompt_with_valid_data() -> None:
    prompt = PromptCreate(
        title="Code Review",
        content="Review this code for correctness.",
        tags=["python", "review"],
    )

    assert prompt.title == "Code Review"
    assert prompt.content == "Review this code for correctness."
    assert prompt.tags == ["python", "review"]


def test_create_prompt_uses_empty_tags_by_default() -> None:
    prompt = PromptCreate(
        title="Summarize",
        content="Summarize the following text.",
    )

    assert prompt.tags == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", ""),
        ("content", ""),
    ],
)
def test_create_prompt_rejects_empty_required_fields(
    field: str,
    value: str,
) -> None:
    data = {
        "title": "Valid title",
        "content": "Valid content",
    }
    data[field] = value

    with pytest.raises(ValidationError):
        PromptCreate(**data)


def test_update_prompt_accepts_partial_data() -> None:
    prompt = PromptUpdate(title="Updated title")

    assert prompt.title == "Updated title"
    assert prompt.content is None
    assert prompt.tags is None


def test_update_prompt_accepts_empty_request() -> None:
    prompt = PromptUpdate()

    assert prompt.title is None
    assert prompt.content is None
    assert prompt.tags is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", ""),
        ("content", ""),
    ],
)
def test_update_prompt_rejects_empty_provided_fields(
    field: str,
    value: str,
) -> None:
    with pytest.raises(ValidationError):
        PromptUpdate(**{field: value})


def test_prompt_response_contains_generated_fields() -> None:
    created_at = datetime(2026, 7, 26, 12, 0, 0, tzinfo=UTC)
    updated_at = datetime(2026, 7, 26, 12, 30, 0, tzinfo=UTC)

    prompt = PromptResponse(
        id=1,
        title="Code Review",
        content="Review this code for correctness.",
        tags=["python", "review"],
        created_at=created_at,
        updated_at=updated_at,
    )

    assert prompt.id == 1
    assert prompt.created_at == created_at
    assert prompt.updated_at == updated_at
