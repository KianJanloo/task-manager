import uuid
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import String

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[int] = mapped_column(default=1, nullable=False)
    due_date: Mapped[str | None] = mapped_column(nullable=True)

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        secondary="note_task",
        back_populates="tasks",
    )
