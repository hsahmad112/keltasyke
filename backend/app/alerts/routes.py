from fastapi import APIRouter, Query
from typing import Optional
from app.db import get_recent_alerts
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["alerts"] )

@router.get("/recent")
async def read_recent_alerts(
    limit: int = Query(default=10, ge=1, le=100, description="Number of alerts to return (1-100)"),
    since: Optional[datetime]=None
):
    return await get_recent_alerts(limit, since)