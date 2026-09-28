from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_recent_alerts
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["alerts"] )

@router.get("/recent")
async def read_recent_alerts(
    limit: int = 10,
    since: Optional[datetime]=None
):
    rows = await get_recent_alerts(limit, since)
    return [dict(row) for row in rows] 