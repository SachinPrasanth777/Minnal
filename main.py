from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
import socketio
from chat.socket import sio
from utilities.database import prisma

app = FastAPI()

socket_app = socketio.ASGIApp(sio, app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")


@app.on_event("startup")
async def startup_event():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()


@app.get("/")
async def test():
    return JSONResponse(content="Hello World 007", status_code=200)


app.mount("/socket.io", socket_app)
