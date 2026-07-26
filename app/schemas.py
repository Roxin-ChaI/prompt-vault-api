from datetime import datetime

from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class PromptUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


class PromptResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
