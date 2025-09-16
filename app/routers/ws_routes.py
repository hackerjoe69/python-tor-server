from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.connection import ConnectionManager, generate_anon_id
from app.redis_pubsub import redis_pubsub
import asyncio
import json

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    anon_id = generate_anon_id()
    await manager.connect(room, websocket)

    # Subscribe to Redis PubSub for this room
    pubsub = await redis_pubsub.subscribe(room)

    try:
        async def reader():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await manager.broadcast(room, message["data"])

        async def writer():
            while True:
                data = await websocket.receive_text()
                payload = json.dumps({"id": anon_id, "msg": data})
                await redis_pubsub.publish(room, payload)

        await asyncio.gather(reader(), writer())

    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
