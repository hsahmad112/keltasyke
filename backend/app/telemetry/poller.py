import httpx
from app.config import settings
from datetime import datetime, timezone
import asyncio
from app.ws.manager import cm
from app.telemetry.cache import vehicle_cache
import logging
logger = logging.getLogger("uvicorn.error")



SLEEP = 250
async def init_polling(broadcast_callback = None):
    #await asyncio.sleep(SLEEP)

    async with httpx.AsyncClient(timeout = 10.0, ) as client:
        while True:
            now = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
            try:
                response = await client.get(settings.SIRI_VM_URL)
                #check statuscode, if 200 unpack the json and access status 
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status')
                    
                    if status == "OK" and isinstance(data.get('result'), dict): #check status, if ok go one step further and access results 
                        result = data['result']

                        if 'vehicles' in result: #if vehicles exist inside results then continue, 
                            vehicles = result['vehicles']
                            logging.info(f"[{now}] {response.status_code}, overwriting previous cache ({len(vehicles)} vehicles)")
                            vehicle_cache.update_vehicles(vehicles)

                            if broadcast_callback:
                                await broadcast_callback()
                        else:
                            logging.warning(f"[{now}] {response.status_code}, result['vehicles'] does not exist, not overwriting previous cache)")

                    elif status in ('PENDING', 'NO_SIRI_DATA'):
                        logger.warning(f"[{now}] SIRI status: {status}, not overwriting previous cache")
                    else:
                        logger.warning(f"[{now}] SIRI status: {status}, unexpected status, not overwriting")
                    
                else:
                    logger.warning(f"[{now}] HTTP {response.status_code}, not overwriting previous cache")
                    
            except asyncio.CancelledError:
                raise
            except httpx.HTTPError as err:
                logger.error(f"[{now}] Poller network error: {type(err).__name__}")
            except Exception:
                logger.exception(f"[{now}] Poller runtime error")
                
            await asyncio.sleep(SLEEP)