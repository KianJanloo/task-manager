from datetime import datetime, timezone

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db

from app.services.user_service import get_user_by_email, create_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_code,
)
from app.schemas.user import UserRegister, UserLogin, UserForgetPass, UserResetPass
from app.models.user import User
from app.models.code import Code

from app.core.exceptions import AlreadyExistsException, UnauthorizedException


def register_service(data: UserRegister, db: Session):
    existing_user = get_user_by_email(db, data.email)

    if existing_user:
        raise AlreadyExistsException("User")

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
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(data.password, user.password_hash):
        raise UnauthorizedException("Invalid email or password")

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


def refresh_service(refresh_token: str, db: Session):
    payload = decode_refresh_token(refresh_token)

    user_id = int(payload["sub"])

    user = db.get(User, user_id)

    if user is None:
        raise UnauthorizedException("User not found")

    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
    }


def forget_pass_service(data: UserForgetPass, db: Session):
    user = get_user_by_email(db, data.email)

    if user is None:
        raise UnauthorizedException("User not found")

    generated_code = generate_code()

    code = Code(code=generated_code, user_id=user.id)

    db.add(code)
    db.commit()
    db.refresh(code)

    return {"code": generated_code}


def reset_pass_service(data: UserResetPass, db: Session):
    user = get_user_by_email(db, data.email)

    if user is None:
        raise UnauthorizedException("User not found")

    code = db.execute(
        select(Code).where(Code.code == data.code, Code.user_id == user.id)
    ).scalar_one_or_none()

    if code is None:
        raise HTTPException(status_code=404, detail="Invalid code")

    if code.expire_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Code expired")

    user.password_hash = hash_password(data.new_password)

    db.delete(code)

    db.commit()
    db.refresh(user)

    return {"message": "Password reset successfully"}
