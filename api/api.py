from fastapi import APIRouter, HTTPException
import asyncio

router = APIRouter()

ping_pong_counter: int = 0
lock = asyncio.Lock()


@router.get('/ping-pong', tags=['ping-pong'])
async def get_ping_counter() -> dict | Exception:
    try:
        global ping_pong_counter
        async with lock:
            ping_pong_counter += 1
        lock.locked()
        return {'pong': ping_pong_counter}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
