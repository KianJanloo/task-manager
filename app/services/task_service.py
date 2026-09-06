from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import CreateTask, UpdateTask


def get_tasks(db: Session):
    return db.execute(
        select(Task)
    ).scalars().all()


def get_task_by_id(db: Session, task_id: int):
    return db.get(Task, task_id)


def create_task(db: Session, data: CreateTask):
    task = Task(**data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(db: Session, task_id: int, data: UpdateTask):
    task = db.get(Task, task_id)

    if task is None:
        return None

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = db.get(Task, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True
