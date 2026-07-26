from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_prompts_by_title_keyword() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["python", "review"],
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Text Summary",
            "content": "Summarize the following article.",
            "tags": ["writing"],
        },
    )

    response = client.get(
        "/prompts/search",
        params={"q": "python"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Code Review"


def test_search_prompts_by_content_keyword() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Code Analysis",
            "content": "Review Python code for correctness.",
            "tags": ["review"],
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Text Summary",
            "content": "Summarize the following article.",
            "tags": ["writing"],
        },
    )

    response = client.get(
        "/prompts/search",
        params={"q": "python"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Code Analysis"


def test_search_prompts_is_case_insensitive() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["python"],
        },
    )

    response = client.get(
        "/prompts/search",
        params={"q": "PYTHON"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Code Review"


def test_search_prompts_returns_empty_list_when_no_match() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["python"],
        },
    )

    response = client.get(
        "/prompts/search",
        params={"q": "translation"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_prompts_filters_by_tag() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["python", "review"],
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Text Summary",
            "content": "Summarize the following article.",
            "tags": ["writing"],
        },
    )

    response = client.get(
        "/prompts",
        params={"tag": "python"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Code Review"


def test_tag_filter_is_case_insensitive() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["Python", "Review"],
        },
    )

    response = client.get(
        "/prompts",
        params={"tag": "PYTHON"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Code Review"


def test_tag_filter_returns_empty_list_when_no_match() -> None:
    client.post(
        "/prompts",
        json={
            "title": "Python Code Review",
            "content": "Review code for correctness.",
            "tags": ["python", "review"],
        },
    )

    response = client.get(
        "/prompts",
        params={"tag": "writing"},
    )

    assert response.status_code == 200
    assert response.json() == []
