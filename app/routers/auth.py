from fastapi import (
    APIRouter,
    Depends,
    Body
)
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.schemas.user import (
    UserResponse,
    UserRegister,
    UserLogin,
    TokenResponse
)
###
from app.services.auth_service import (
    register_service,
    login_service,
    refresh_service
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserResponse)
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    return register_service(data, db)


@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    return login_service(data, db)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    return refresh_service(refresh_token, db)
