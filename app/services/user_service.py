from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User

from pydantic import EmailStr


def get_user_by_email(db: Session, email: EmailStr):
    return db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

def create_user(db: Session, email: EmailStr, password_hash: str):
    user = User(
        email=email,
        password_hash=password_hash
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user