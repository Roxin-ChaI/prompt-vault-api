# Prompt Vault API

[English](README.md) | [简体中文](README.zh-CN.md)

A REST API for storing, searching, updating, and organizing reusable prompts.

The project demonstrates a complete backend development workflow using FastAPI, SQLAlchemy, SQLite, Alembic, pytest, Ruff, Docker, Docker Compose, and GitHub Actions.

## Features

- Create reusable prompts
- List all prompts
- Retrieve a prompt by ID
- Update existing prompts
- Delete prompts
- Search prompts by title or content
- Filter prompts by tag
- Persist data with SQLite
- Manage database schema changes with Alembic
- Run automated tests with pytest
- Check code quality with Ruff
- Run the application with Docker
- Run continuous integration with GitHub Actions

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- pytest
- Ruff
- Docker
- Docker Compose
- GitHub Actions

## Project Structure

```text
prompt-vault-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── database.py
│   ├── dependencies.py
│   ├── init_db.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── docs/
│   └── requirements.md
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_schemas.py
│   └── test_search.py
├── .dockerignore
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
└── README.zh-CN.md
```

## Local Development

### 1. Create a virtual environment

```bash
python3.12 -m venv .venv
```

### 2. Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev]"
```

### 4. Apply database migrations

```bash
alembic upgrade head
```

This creates the local SQLite database and the required tables.

### 5. Start the API server

```bash
uvicorn app.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Check whether the API is running |
| `POST` | `/prompts` | Create a prompt |
| `GET` | `/prompts` | List prompts |
| `GET` | `/prompts?tag={tag}` | Filter prompts by tag |
| `GET` | `/prompts/search?q={query}` | Search prompts |
| `GET` | `/prompts/{prompt_id}` | Retrieve a prompt |
| `PUT` | `/prompts/{prompt_id}` | Update a prompt |
| `DELETE` | `/prompts/{prompt_id}` | Delete a prompt |

## Example Request

Create a prompt:

```bash
curl -X POST http://127.0.0.1:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review",
    "content": "Review the following code and identify potential problems.",
    "tags": ["development", "review"]
  }'
```

Example response:

```json
{
  "id": 1,
  "title": "Code Review",
  "content": "Review the following code and identify potential problems.",
  "tags": [
    "development",
    "review"
  ],
  "created_at": "2026-07-26T12:00:00",
  "updated_at": "2026-07-26T12:00:00"
}
```

## Database Migrations

Apply all migrations:

```bash
alembic upgrade head
```

Display the current migration version:

```bash
alembic current
```

Roll back all migrations:

```bash
alembic downgrade base
```

Reapply all migrations:

```bash
alembic upgrade head
```

## Testing

Run the complete test suite:

```bash
python -m pytest -q
```

Run the Ruff code-quality check:

```bash
ruff check app tests migrations
```

Check for whitespace errors:

```bash
git diff --check
```

## Docker

### Build the image

```bash
docker build -t prompt-vault-api .
```

### Run the container

```bash
docker run --rm \
  --name prompt-vault-api \
  -p 8000:8000 \
  prompt-vault-api
```

The container applies the latest Alembic migrations before starting the API server.

## Docker Compose

Build and start the service:

```bash
docker compose up --build
```

Start the service in the background:

```bash
docker compose up -d --build
```

Display the service status:

```bash
docker compose ps
```

Stop and remove the service:

```bash
docker compose down
```

## Continuous Integration

The GitHub Actions workflow runs automatically for pushes and pull requests.

The CI workflow performs the following checks:

1. Sets up Python 3.12
2. Installs the project and development dependencies
3. Runs Ruff
4. Runs the pytest test suite
5. Tests Alembic upgrade and downgrade operations

## Current Scope

The current version intentionally does not include:

- User authentication
- Authorization
- A frontend interface
- Cloud deployment
- Multiple database backends

These features are outside the initial project requirements.
