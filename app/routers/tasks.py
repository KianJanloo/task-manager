from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import CreateTask, UpdateTask, TaskResponse
from app.services.task_service import (
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    get_tasks,
)

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
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.post("/", response_model=TaskResponse)
def create_task_endpoint(
    task: CreateTask,
    db: Session = Depends(get_db),
):
    return create_task(db, task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    data: UpdateTask,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.delete("/{task_id}")
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {"message": "Task deleted"}
