import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.telemetry.cache import vehicle_cache  # Adjust path as needed
from app.ws.manager import cm

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/buses")
async def websocket_buses(websocket: WebSocket):
    await cm.connect(websocket)
    try:
        #build and send initial snapshot
        await websocket.send_json(build_vehicle_payload())
        cm.register(websocket)

        while True:
            data = await websocket.receive_json()

            if isinstance(data, dict) and data.get("type") == "location":
                lat, lng = data.get("lat"), data.get("lng")
                if lat is not None and lng is not None:
                    cm.update_location(websocket, float(lat), float(lng))

    except WebSocketDisconnect:
        logger.info("Client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket session error: {e}")
    finally:
        cm.disconnect(websocket)



async def broadcast_vehicle_update():
    payload = build_vehicle_payload() #takes last snapshot
    await cm.broadcast(payload) #broadcasts to all active clients



def build_vehicle_payload() -> dict:
    "Helper, builds vehicle state message from memory"
    return {
        "type": "vehicles",
        "vehicles": vehicle_cache.get_all_vehicles(),
        "last_updated": vehicle_cache.get_last_updated().isoformat(),
    }