from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
