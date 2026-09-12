from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.schemas.user import (
    UserResponse,
    UserRegister,
    UserLogin,
    TokenResponse,
    UserForgetPass,
    UserResetPass,
)

from app.services.auth_service import (
    register_service,
    login_service,
    refresh_service,
    forget_pass_service,
    reset_pass_service,
)
from app.core.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_service(data, db)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_service(data, db)


@router.post(
    "/refresh", response_model=TokenResponse, dependencies=[
        Depends(get_current_user)
    ]
)
def refresh(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return refresh_service(refresh_token, db)


@router.post("/forget-pass")
def forgetPass(data: UserForgetPass, db: Session = Depends(get_db)):
    return forget_pass_service(data, db)


@router.post("/reset-pass")
def resetPass(data: UserResetPass, db: Session = Depends(get_db)):
    return reset_pass_service(data, db)
