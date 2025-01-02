from fastapi import HTTPException
from utilities.redis import cache_service
import socketio
from datetime import datetime
from middlewares.dependency import get_current_user

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])


@sio.event
async def connect(sid, environ):
    try:
        auth_header = environ.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="No token provided")

        token = auth_header.split(" ")[1]
        user = await get_current_user(token)
        await sio.save_session(sid, {"user": user})
        await sio.emit("welcome", {"data": f"Welcome {user.email}!"}, room=sid)
    except HTTPException:
        await sio.disconnect(sid)
        return False


@sio.event
async def disconnect(sid):
    session = await sio.get_session(sid)
    user = session.get("user")
    print(f"Client disconnected: {sid} ({user.email if user else 'unauthorized'})")


@sio.event
async def join_room(sid, data):
    session = await sio.get_session(sid)
    user = session.get("user")
    room = data.get("room")

    await sio.enter_room(sid, room)
    print(f"Client {user.email} joined room: {room}")

    chat_history = await cache_service.get(f"chat_history:{room}")
    if chat_history:
        for msg in chat_history:
            await sio.emit(
                "message",
                {
                    "user": msg["user"],
                    "message": msg["content"],
                    "timestamp": msg["timestamp"],
                },
                room=sid,
            )

    await sio.emit("joined", {"room": room, "user": user.email}, room=room)


@sio.event
async def chat_message(sid, data):
    session = await sio.get_session(sid)
    user = session.get("user")
    room = data.get("room")
    message = data.get("message")
    timestamp = datetime.now().isoformat()

    message_data = {"user": user.email, "content": message, "timestamp": timestamp}

    stored_message = {"user": user.email, "message": message, "timestamp": timestamp}

    await cache_service.set(f"chat:{room}:{sid}", message_data, expire=None)
    chat_history_key = f"chat_history:{room}"
    chat_history = await cache_service.get(chat_history_key) or []
    chat_history.append(message_data)
    await cache_service.set(chat_history_key, chat_history, expire=None)

    await sio.emit("message", stored_message, room=room)


app = socketio.ASGIApp(sio)
