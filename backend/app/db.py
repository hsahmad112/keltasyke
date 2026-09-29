from contextlib import asynccontextmanager
import asyncpg, logging
from .config import settings

_pool = None

logger = logging.getLogger("uvicorn.error")

async def init_pool():
    global _pool
    if _pool is None:
        dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PWD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        _pool = await asyncpg.create_pool(dsn=dsn, min_size = 1, max_size = 5)
        print('Pool initialized')

@asynccontextmanager
async def get_conn():
    # global _pool #supuerflous no? get_conn only uses _pool, never assigns
    if _pool is None: #refers to module level variable
        raise RuntimeError('Pool is not initialized')
    async with _pool.acquire() as conn:
        yield conn #yielding to API route

async def close_pool():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        print('Pool\'s closed')

    

async def load_preferences():
    async with get_conn() as conn:
        query = "Select * from preferences where id = 1"
        row = await conn.fetchrow(query)
        if row is None:
            return {"id": 1, "lines": [], "stops": [], "updated_at": None} #fallback, should be backends responsibility
        res = dict(row)
        res["lines"] = res["lines"] or []
        res["stops"] = res["stops"] or []
        logger.info(f"loaded user pref from db")
        return res

async def save_preferences(lines, stops):
    async with get_conn() as conn:
        query = """INSERT INTO preferences (id, lines, stops, updated_at) VALUES (1, $1, $2, NOW()) ON CONFLICT (id) 
        DO UPDATE SET
            lines = EXCLUDED.lines,
            stops = EXCLUDED.stops,
            updated_at = NOW()
        RETURNING *;
        """
        row = await conn.fetchrow(query, lines, stops)
        logger.info(f"saved user pref to db")

        return dict(row) if row else None
 

async def get_recent_alerts(limit, since):
    async with get_conn() as conn:
        query = """SELECT id, summary_en, raw_text, created_at FROM service_alerts 
        WHERE $2::timestamptz is NULL OR created_at > $2::timestamptz
        ORDER BY created_at DESC 
        LIMIT $1 ;"""
        rows = await conn.fetch(query, limit, since)
        logger.info(f"retrieved recent alerts")
        return [dict(r) for r in rows]