from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import CreateTask, UpdateTask, TaskResponse
from app.services.task_service import (
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    get_tasks,
)

from app.core.exceptions import NotFoundException
from app.schemas.note import NoteResponse
from app.core.security import get_current_user, require_role
from uuid import UUID

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/", response_model=list[TaskResponse])
def get_tasks_endpoint(
    db: Session = Depends(get_db),
):
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise NotFoundException("Task", task_id)

    return task


@router.get("/{task_id}/notes", response_model=list[NoteResponse])
def get_task_notes(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise NotFoundException("Task", task_id)

    return task.notes


@router.post(
    "/",
    response_model=TaskResponse,
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def create_task_endpoint(
    task: CreateTask,
    db: Session = Depends(get_db),
):
    return create_task(db, task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def update_task_endpoint(
    task_id: UUID,
    data: UpdateTask,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, data)

    if task is None:
        raise NotFoundException("Task", task_id)

    return task


@router.delete(
    "/{task_id}",
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def delete_task_endpoint(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise NotFoundException("Task", task_id)

    return {"message": "Task deleted"}
