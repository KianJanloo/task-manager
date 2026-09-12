from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from enum import Enum


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserForgetPass(BaseModel):
    email: EmailStr


class UserResetPass(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6)
    new_password: str = Field(min_length=8)


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class ChangeRole(BaseModel):
    role: UserRole
