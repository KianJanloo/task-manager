from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from pydantic import EmailStr

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[EmailStr] = mapped_column(
        String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
