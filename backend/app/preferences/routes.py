from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.db import load_preferences, save_preferences
from app.preferences.cache import preferences_cache

router = APIRouter(prefix="/preferences", tags=["preferences"] )


class PreferencesUpdate(BaseModel):
    lines: List[str]
    stops: List[str]


@router.get("")
async def read_preferences():
    return await load_preferences()

@router.put("")
async def put_preferences(body: PreferencesUpdate):
    print(f" This is the actual {body} recieved ")

    res = await save_preferences(body.lines, body.stops) #method returns RETURNING *, and thats what res is

    preferences_cache.set_preferences(res)
    return preferences_cache.get_preferences()

    