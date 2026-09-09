from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr


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
    