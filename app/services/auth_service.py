from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db

from app.services.user_service import get_user_by_email, create_user
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.schemas.user import UserResponse, UserRegister, UserLogin, TokenResponse
from app.models.user import User


def register_service(data: UserRegister, db: Session):
    existing_user = get_user_by_email(db, data.email)

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    password_hash = hash_password(data.password)

    user = create_user(
        db,
        data.email,
        password_hash,
    )

    return user


def login_service(data: UserLogin, db: Session):
    user = get_user_by_email(db, data.email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


def refresh_service(
    refresh_token: str,
    db: Session
):
    payload = decode_refresh_token(refresh_token)

    user_id = int(payload["sub"])

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
    }