from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utilities.database import prisma
from routes.auth import auth_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def test():
    return JSONResponse(content="Hello World 007", status_code=200)
