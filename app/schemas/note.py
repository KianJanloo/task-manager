from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID


class CreateNote(BaseModel):
    title: str
    description: str | None = None


class NoteResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    

class UpdateNote(BaseModel):
    title: str | None = None
    description: str | None = None
