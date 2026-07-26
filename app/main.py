from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.dependencies import get_db
from app.models import Prompt
from app.schemas import PromptCreate, PromptResponse, PromptUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Prompt Vault API",
    version="0.1.0",
)

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Prompt Vault API"}


@app.post(
    "/prompts",
    response_model=PromptResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prompt(
    prompt: PromptCreate,
    db: DbSession,
) -> Prompt:
    db_prompt = Prompt(
        title=prompt.title,
        content=prompt.content,
        tags=prompt.tags,
    )

    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)

    return db_prompt


@app.get(
    "/prompts",
    response_model=list[PromptResponse],
)
def list_prompts(
    db: DbSession,
    tag: str | None = None,
) -> list[Prompt]:
    statement = select(Prompt).order_by(Prompt.id)
    stored_prompts = list(db.scalars(statement).all())

    if tag is None:
        return stored_prompts

    normalized_tag = tag.casefold()

    return [
        prompt
        for prompt in stored_prompts
        if any(
            prompt_tag.casefold() == normalized_tag
            for prompt_tag in prompt.tags
        )
    ]


@app.get(
    "/prompts/search",
    response_model=list[PromptResponse],
)
def search_prompts(
    q: str,
    db: DbSession,
) -> list[Prompt]:
    pattern = f"%{q}%"

    statement = (
        select(Prompt)
        .where(
            or_(
                Prompt.title.ilike(pattern),
                Prompt.content.ilike(pattern),
            )
        )
        .order_by(Prompt.id)
    )

    return list(db.scalars(statement).all())


@app.get(
    "/prompts/{prompt_id}",
    response_model=PromptResponse,
)
def get_prompt(
    prompt_id: int,
    db: DbSession,
) -> Prompt:
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )

    return prompt


@app.put(
    "/prompts/{prompt_id}",
    response_model=PromptResponse,
)
def update_prompt(
    prompt_id: int,
    prompt_update: PromptUpdate,
    db: DbSession,
) -> Prompt:
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )

    update_data = prompt_update.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in update_data.items():
        setattr(prompt, field, value)

    prompt.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(prompt)

    return prompt


@app.delete(
    "/prompts/{prompt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_prompt(
    prompt_id: int,
    db: DbSession,
) -> None:
    prompt = db.get(Prompt, prompt_id)

    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )

    db.delete(prompt)
    db.commit()
