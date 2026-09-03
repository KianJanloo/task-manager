from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

users = []


@router.post('/auth/register', response_model=UserResponse)
def register(user: UserCreate):
    new_user = {
        "id": len(users) + 1,
        "email": user.email,
        "name": user.name,
    }

    users.append(new_user)
    return new_user


def get_current_user():
    return {
        "id": 1,
        "email": "ali@example.com",
        "name": "Ali",
    }

@router.get('/me', response_model=UserResponse)
def get_me(user=Depends(get_current_user)):
    return user