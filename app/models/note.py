from datetime import datetime, timezone

from app.db.database import Base

from sqlalchemy import Column, ForeignKey, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

note_task = Table(
    "note_task",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=note_task,
        back_populates="notes",
    )
