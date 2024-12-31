from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from utilities.database import prisma
from schema.models import UserSignUp, UserLogin, User
from utilities.hash import Hash
from utilities.redis import CacheConfig, CacheService
from middlewares.dependency import get_current_user
from dotenv import load_dotenv
from uuid import UUID
import logging
import json
import os

load_dotenv()
auth_router = APIRouter()
cache_config = CacheConfig(REDIS_URL=os.getenv("REDIS_URL"), REDIS_DB=0)
cache_service = CacheService(cache_config)


@auth_router.on_event("startup")
async def startup_event():
    await cache_service.initialize()


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
        if existing_user is None:
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        password_valid = Hash().check_password(user.password, existing_user.password)
        if not password_valid:
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        token = Hash().generate_token(user.email)
        return JSONResponse(content={"token": token}, status_code=200)
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        raise HTTPException(detail="Login Failed", status_code=400)


@auth_router.get("/user/{id}")
async def get_user(id: UUID, current_user: User = Depends(get_current_user)):
    try:
        print(f"Retrieving user with ID: {id}")
        cache_key = f"user:{id}"
        cached_user = await cache_service.get(cache_key)

        if cached_user:
            print(f"Cache hit for user ID: {id}")
            return JSONResponse(content=json.loads(cached_user), status_code=200)

        print(f"Cache miss for user ID: {id}")
        user = await prisma.prisma.user.find_unique(where={"id": str(id)})

        if not user:
            print(f"User not found for ID: {id}")
            raise HTTPException(status_code=404, detail="User not found")

        await cache_service.set(
            cache_key,
            json.dumps(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
            ),
        )
        print(f"User ID: {id} retrieved from database and cached.")

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
