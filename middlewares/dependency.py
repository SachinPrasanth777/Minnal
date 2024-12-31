from fastapi import Depends, HTTPException
import jwt
from schema.models import User
from middlewares.bearer import JWTBearer
import os
from dotenv import load_dotenv
from utilities.database import prisma

load_dotenv()


async def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(token, os.getenv("SECRET"), algorithms=["HS256"])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await prisma.prisma.user.find_unique(where={"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except (jwt.PyJWTError, AttributeError):
        return HTTPException(status_code="403", detail="Not Authorized")
