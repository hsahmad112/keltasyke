from fastapi import WebSocket
from typing import List, Dict
import logging

logger = logging.getLogger("uvicorn.error")


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.client_locations: Dict[WebSocket, Dict[str, float]] = {}


    async def connect(self, websocket:WebSocket):
        await websocket.accept()

    def register(self, websocket: WebSocket):
        if websocket not in self.active_connections:
            self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.client_locations.pop(websocket, None)

    async def broadcast(self, payload):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(payload)
            except Exception as e:
                logger.warning(f"Failed to send to client, removing socket: {e}")
                self.disconnect(connection)
    
    def update_location(self, websocket: WebSocket, lat: float, lng: float):
        self.client_locations[websocket] = {"lat": lat, "lng": lng}

    def get_locations(self) -> List[Dict[str, float]]:
        logger.info(self.client_locations.values())
        return list(self.client_locations.values())
    

cm = ConnectionManager()