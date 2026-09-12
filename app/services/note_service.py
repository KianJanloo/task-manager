from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.core.exceptions import NotFoundException
from app.schemas.note import CreateNote, UpdateNote
from app.models.task import Task

from datetime import datetime, timezone
from uuid import UUID


def get_notes_service(db: Session, page: int = 1, limit: int = 100):
    skip = (page - 1) * limit

    return db.execute(select(Note).offset(skip).limit(limit)).scalars().all()


def get_note_service(db: Session, note_id: UUID):
    note = db.execute(select(Note).where(Note.id == note_id)).scalar_one_or_none()

    if note is None:
        raise NotFoundException("note", note_id)

    return note


def create_note_service(db: Session, data: CreateNote):
    note = Note(**data.model_dump())

    db.add(note)
    db.commit()

    db.refresh(note)
    return note


def assign_note_to_task_service(db: Session, note_id: UUID, task_id: UUID):
    note = get_note_service(db, note_id)
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()

    if task is None:
        raise NotFoundException("task", task_id)

    note.tasks.append(task)
    db.commit()
    db.refresh(note)

    return note


def update_note_service(db: Session, note_id: UUID, data: UpdateNote):
    note = get_note_service(db, note_id)

    note.updated_at = datetime.now(timezone.utc)

    for key, value in data.model_dump().items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return note


def delete_note_service(db: Session, note_id: UUID):
    note = get_note_service(db, note_id)

    db.delete(note)
    db.commit()
    db.refresh(note)

    return {"message": f"Note with id {note_id} has been deleted successfully."}
