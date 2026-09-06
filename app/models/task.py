from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy import String

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[int] = mapped_column(default=1, nullable=False)
    due_date: Mapped[str | None] = mapped_column(nullable=True)
