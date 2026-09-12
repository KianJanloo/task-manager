import os

import jwt
from jwt import InvalidTokenError

from dotenv import load_dotenv
from pwdlib import PasswordHash

from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException

from app.db.database import get_db
from sqlalchemy.orm import Session

from app.models.user import User

from datetime import datetime, timedelta, timezone

import secrets

from uuid import UUID

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

oauth2_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


def get_current_user(credentials=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    user_id = UUID(payload.get("sub"))

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

    return user


def require_role(*allowed_roles: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this resource",
            )
        return user

    return role_checker


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return payload

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def generate_code():
    return f"{secrets.randbelow(1_000_000):06d}"
