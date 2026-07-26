from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, status

from app.schemas import PromptCreate, PromptResponse, PromptUpdate

app = FastAPI(
    title="Prompt Vault API",
    version="0.1.0",
)

prompts: list[PromptResponse] = []


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Prompt Vault API"}


@app.post(
    "/prompts",
    response_model=PromptResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prompt(prompt: PromptCreate) -> PromptResponse:
    now = datetime.now(UTC)

    created_prompt = PromptResponse(
        id=len(prompts) + 1,
        title=prompt.title,
        content=prompt.content,
        tags=prompt.tags,
        created_at=now,
        updated_at=now,
    )

    prompts.append(created_prompt)

    return created_prompt


@app.get(
    "/prompts",
    response_model=list[PromptResponse],
)
def list_prompts() -> list[PromptResponse]:
    return prompts

@app.get(
    "/prompts/{prompt_id}",
    response_model=PromptResponse,
)
def get_prompt(prompt_id: int) -> PromptResponse:
    for prompt in prompts:
        if prompt.id == prompt_id:
            return prompt

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Prompt not found",
    )

@app.put(
    "/prompts/{prompt_id}",
    response_model=PromptResponse,
)
def update_prompt(
    prompt_id: int,
    prompt_update: PromptUpdate,
) -> PromptResponse:
    for index, prompt in enumerate(prompts):
        if prompt.id != prompt_id:
            continue

        update_data = prompt_update.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        updated_prompt = PromptResponse(
            id=prompt.id,
            title=update_data.get("title", prompt.title),
            content=update_data.get("content", prompt.content),
            tags=update_data.get("tags", prompt.tags),
            created_at=prompt.created_at,
            updated_at=datetime.now(UTC),
        )

        prompts[index] = updated_prompt

        return updated_prompt

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Prompt not found",
    )















