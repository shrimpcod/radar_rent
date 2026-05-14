from fastapi import WebSocket
import json 

class ConnectionManager:
    def __init__(self):
        self.activate_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activate_connection.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.activate_connection:
            await connection.send_text(json.dumps(data))
        
ws_manager = ConnectionManager()