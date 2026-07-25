# Prompt Vault API Requirements

## 1. Project Goal

Build a REST API for managing reusable prompts.

The API should allow users to create, retrieve, update, delete, and search prompts.

## 2. Prompt Data

Each prompt contains:

* `id`
* `title`
* `content`
* `tags`
* `created_at`
* `updated_at`

## 3. Core Features

The system must support:

1. Create a prompt
2. List all prompts
3. Retrieve a prompt by ID
4. Update a prompt
5. Delete a prompt
6. Search prompts by keyword
7. Filter prompts by tag

## 4. Technical Requirements

* Python
* FastAPI
* SQLite
* Pytest
* Ruff
* Docker
* GitHub Actions

## 5. Current Scope

The first version will not include:

* User accounts
* Authentication
* Web frontend
* Cloud deployment
* Multiple databases

