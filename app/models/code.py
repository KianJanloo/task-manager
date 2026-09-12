import uuid
from uuid import UUID

from app.db.database import Base

from datetime import datetime, timezone, timedelta

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Code(Base):
    __tablename__ = "codes"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
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
