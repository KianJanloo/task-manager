from fastapi import APIRouter, Depends
from app.schemas.user import ChangeRole, UserResponse
from app.core.security import get_current_user, require_role
from sqlalchemy.orm import Session
from app.db.database import get_db
from uuid import UUID
from app.services.user_service import change_role
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.patch(
    "/{user_id}/change_role",
    response_model=UserResponse,
    dependencies=[
        Depends(get_current_user),
        Depends(require_role("admin")),
    ],
)
def change_role_endpoint(
    user_id: UUID,
    role: ChangeRole,
    db: Session = Depends(get_db),
):
    return change_role(db, user_id, role)


@router.get("/me", response_model=UserResponse)
def get_me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user