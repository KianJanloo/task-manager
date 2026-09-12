from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User

from pydantic import EmailStr
from uuid import UUID
from app.core.exceptions import NotFoundException


def get_user_by_email(db: Session, email: EmailStr):
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def create_user(db: Session, email: EmailStr, password_hash: str):
    user = User(email=email, password_hash=password_hash)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def change_role(db: Session, user_id: UUID, role: str):
    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()

    if (user is None):
        raise NotFoundException("user", user_id)

    user.role = role
    db.commit()
    db.refresh(user)

    return user
