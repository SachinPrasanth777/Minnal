from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from utilities.database import prisma
from schema.models import UserSignUp, UserLogin, User
from utilities.hash import Hash
from middlewares.dependency import get_current_user
from uuid import UUID
import logging

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(user: UserSignUp):
    try:
        password = Hash().hash_password(user.password)
        new_user = await prisma.prisma.user.create(
            data={
                "username": user.username,
                "email": user.email,
                "password": password,
            }
        )
        return JSONResponse(
            content={
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
            },
            status_code=201,
        )
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(detail="Failed to create user", status_code=400)


@auth_router.post("/login")
async def login(user: UserLogin):
    try:
        existing_user = await prisma.prisma.user.find_unique(
            where={"email": user.email}
        )
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        password = Hash().check_password(user.password, existing_user.password)
        if not password:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        token = Hash().generate_token(user.email)
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        raise HTTPException(detail="Login Failed", status_code=400)


@auth_router.get("/user/{id}")
async def get_user(id: UUID, current_user: User = Depends(get_current_user)):
    try:
        user = await prisma.prisma.user.find_unique(where={"id": str(id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(
            content={
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
            status_code=200,
        )
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Server error")
