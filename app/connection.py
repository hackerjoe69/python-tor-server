import uuid
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # room_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def broadcast(self, room: str, message: str):
        if room in self.active_connections:
            for conn in self.active_connections[room]:
                await conn.send_text(message)

def generate_anon_id() -> str:
    return str(uuid.uuid4())
