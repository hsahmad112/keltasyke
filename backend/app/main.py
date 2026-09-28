import asyncpg
from fastapi import FastAPI
from app import db
from contextlib import asynccontextmanager

from app.alerts.routes import router as alerts_router
from app.preferences.routes import router as preferences_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_pool()
    yield
    await db.close_pool()    

app = FastAPI(lifespan = lifespan)
app.include_router(alerts_router)
app.include_router(preferences_router)

@app.get("/")
async def root():
    return{'message': f"We are live"}