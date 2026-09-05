from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.services.user_service import get_user_by_email, create_user
from app.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserResponse, UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserResponse)
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, data.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    password_hash = hash_password(data.password)

    user = create_user(
        db,
        data.email,
        password_hash,
    )

    return user


@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
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
        "token_type": "bearer",
    }
