import uuid
from uuid import UUID

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from pydantic import EmailStr

from app.db.database import Base
from app.schemas.user import UserRole

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[EmailStr] = mapped_column(
        String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=UserRole.user,
    )
    
    codes: Mapped[list["Code"]] = relationship(
        back_populates="user"
    )
