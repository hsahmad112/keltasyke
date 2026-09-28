from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.db import get_preferences, update_preferences

router = APIRouter(prefix="/preferences", tags=["preferences"] )


class PrefencesUpdate(BaseModel):
    lines: List[str]
    stops: List[int]


@router.get("")
async def read_preferences():
    return await get_preferences()

@router.put("")
async def save_preferences(body: PrefencesUpdate):
    print(f" This is the actual {body} recieved ")
    return await update_preferences(body.lines, body.stops)
    