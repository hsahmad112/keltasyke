import asyncpg, asyncio
from fastapi import FastAPI
from app import db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. Import CORSMiddleware


from app.alerts.routes import router as alerts_router
from app.preferences.routes import router as preferences_router
from app.db import load_preferences
from app.telemetry.poller import init_polling
from app.telemetry.cache import vehicle_cache
from app.preferences.cache import preferences_cache
from app.ws.routes import broadcast_vehicle_update
from app.ws.routes import router as ws_router
from app.ws.manager import cm



@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_pool()
    poller_task = asyncio.create_task(init_polling(broadcast_callback=broadcast_vehicle_update))
    
    initial_prefs = await load_preferences()
    preferences_cache.set_preferences(initial_prefs)
    yield
    
    poller_task.cancel()
    try:
        await poller_task
    except asyncio.CancelledError:
        pass
    await db.close_pool()    

app = FastAPI(lifespan = lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts_router)
app.include_router(preferences_router)
app.include_router(ws_router) 



@app.get("/")
async def root():
    return{'message': f"We are live"}


@app.get("/debug/vehicles")
def debug_vehicles(sample_size: int = 1):
    all_vehicles = vehicle_cache.get_all_vehicles()
    
    has_none_entries = any(v is None for v in all_vehicles)
    
    sample = all_vehicles[:sample_size]
    

    return {
        "total_cache_count": len(all_vehicles),
        "last_updated": vehicle_cache.get_last_updated(),
        "has_none_entries": has_none_entries,
        "sample": sample,
    }

@app.get("/debug/locations")
def debug_locations():
    return {
        "active_clients": len(cm.active_connections),
        "locations": cm.get_locations()
    }