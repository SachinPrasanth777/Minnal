from pydantic import BaseModel
import uuid


class UserSignUp(BaseModel):
    username: str
    email: str
    password: str
