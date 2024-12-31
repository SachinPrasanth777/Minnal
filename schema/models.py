from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
