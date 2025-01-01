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
    await sio.emit("joined", {"room": room}, room=room)


@sio.event
async def chat_message(sid, data):
    room = data.get("room")
    message = data.get("message")
    print(f"Message from {sid} in room {room}: {message}")
    await sio.emit("message", {"message": message}, room=room)
