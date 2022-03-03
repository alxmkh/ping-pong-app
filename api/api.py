from fastapi import APIRouter, HTTPException
import asyncio

router = APIRouter()

ping_pong_counter: int = 0
lock = asyncio.Lock()

file_path = '/usr/src/app/files/timestamp.db'


@router.get('/pp-get-data-from-file', tags=['ping-pong'])
async def get_ping_counter_from_file() -> dict | Exception:
    try:
        global ping_pong_counter
        async with lock:
            ping_pong_counter += 1
        with open(file_path, 'w', encoding='utf-8') as fr:
            fr.write(f'Ping / Pongs: {ping_pong_counter}')
        return {'pong': ping_pong_counter}
    except Exception as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get('/pp-get-data-from-rest', tags=['ping-pong'])
async def get_ping_counter_from_rest() -> dict | Exception:
    try:
        global ping_pong_counter
        async with lock:
            ping_pong_counter += 1
        return {'pong': ping_pong_counter}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
