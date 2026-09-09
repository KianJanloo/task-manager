from app.db.database import Base

from datetime import datetime, timezone, timedelta

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Code(Base):
    __tablename__ = "codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    expire_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    user: Mapped["User"] = relationship(
        back_populates="codes"
    )
