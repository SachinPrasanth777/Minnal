from utilities.redis import cache_service
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("welcome", {"data": "Welcome to the chat!"}, room=sid)


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def join_room(sid, data):
    room = data.get("room")
    await sio.enter_room(sid, room)
    print(f"Client {sid} joined room: {room}")
    chat_history = await cache_service.get(f"chat_history:{room}")
    if chat_history:
        for message in chat_history:
            await sio.emit("message", {"message": message}, room=sid)
    await sio.emit("joined", {"room": room}, room=room)


@sio.event
async def chat_message(sid, data):
    room = data.get("room")
    message = data.get("message")
    print(f"Message from {sid} in room {room}: {message}")
    await cache_service.set(f"chat:{room}:{sid}", message, expire=None)
    chat_history_key = f"chat_history:{room}"
    chat_history = await cache_service.get(chat_history_key) or []
    chat_history.append(message)
    await cache_service.set(chat_history_key, chat_history, expire=None)
    await sio.emit("message", {"message": message}, room=room)
