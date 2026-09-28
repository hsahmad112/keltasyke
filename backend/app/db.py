from contextlib import asynccontextmanager
import asyncpg
from .config import settings

_pool = None

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
    print('Pool closed')
    

async def get_preferences():
    async with get_conn() as conn:
        query = "Select * from preferences where id = 1"
        row = await conn.fetchrow(query)
        if row is None:
            return {"id": 1, "lines": [], "stops": []} #fallback, should be backends responsibility
        return row

async def update_preferences(lines, stops):
    async with get_conn() as conn:
        query = """INSERT INTO preferences (id, lines, stops, updated_at) VALUES (1, $1, $2, NOW()) ON CONFLICT (id) 
        DO UPDATE SET
            lines = EXCLUDED.lines,
            stops = EXCLUDED.stops,
            updated_at = NOW()
        RETURNING *;
        """
        row = await conn.fetchrow(query, lines, stops)
        return row


async def get_recent_alerts(limit, since):
    async with get_conn() as conn:
        query = """SELECT * FROM service_alerts 
        WHERE $2 is NULL OR created_at > $2 
        ORDER BY created_at DESC 
        LIMIT $1 ;"""
        rows = await conn.fetch(query, limit, since)
        return rows