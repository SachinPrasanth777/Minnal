from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from utilities.database import PrismaClient
from schema.models import UserSignUp

app = FastAPI()
prisma = PrismaClient()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.post("/user")
async def create_user(user: UserSignUp):
    try:
        new_user = await prisma.user.create(
            data={
                "username": user.username,
                "email": user.email,
                "password": user.password,
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
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create user")


@app.get("/")
async def test():
    return JSONResponse(content="Hello World 007", status_code=200)
