from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.services.note_service import (
    assign_note_to_task_service,
    create_note_service,
    delete_note_service,
    get_note_service,
    get_notes_service,
    update_note_service,
)
from sqlalchemy.orm import Session
from app.schemas.note import CreateNote, UpdateNote
from app.core.security import get_current_user, require_role

from uuid import UUID

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.get("/")
def get_notes(db: Session = Depends(get_db), page: int = 1, limit: int = 100):
    notes = get_notes_service(db, page, limit)
    return notes


@router.get("/{note_id}")
def get_note(note_id: UUID, db: Session = Depends(get_db)):
    note = get_note_service(db, note_id)
    return note


@router.post(
    "/",
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def create_note(data: CreateNote, db: Session = Depends(get_db)):
    note = create_note_service(db, data)
    return note


@router.post(
    "/{note_id}/assign/{task_id}",
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def assign_note_to_task(
    note_id: UUID, task_id: UUID, db: Session = Depends(get_db)
):
    note = assign_note_to_task_service(db, note_id, task_id)
    return note


@router.put(
    "/{note_id}",
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def update_note(note_id: UUID, data: UpdateNote, db: Session = Depends(get_db)):
    note = update_note_service(db, note_id, data)
    return note


@router.delete(
    "/{note_id}",
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def delete_note(note_id: UUID, db: Session = Depends(get_db)):
    result = delete_note_service(db, note_id)
    return result
