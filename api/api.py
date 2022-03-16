from fastapi import APIRouter, HTTPException, Depends
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from databases import models, crud, schemas
from databases.database import SessionLocal, engine

load_dotenv()

router = APIRouter()

ping_pong_counter: int = 0
lock = asyncio.Lock()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/pp-get-data-from-file', tags=['ping-pong'])
async def get_ping_counter_from_file() -> dict | Exception:
    try:
        global ping_pong_counter
        async with lock:
            ping_pong_counter += 1
        with open(os.getenv("MOUNT"), 'w', encoding='utf-8') as fr:
            fr.write(f'Ping / Pongs: {ping_pong_counter}')
        return {'pong': ping_pong_counter}
    except Exception as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get('/pp-get-data-from-rest', tags=['ping-pong'])
async def get_ping_counter_from_rest(db: Session = Depends(get_db)) -> dict | Exception:
    try:
        flag = crud.get_current_counter(db)
        if not flag:
            crud.insert_counter(db)
        current_count_value = crud.increment_counter(db)
        # global ping_pong_counter
        # async with lock:
        #     ping_pong_counter += 1
        return {"pong": current_count_value.ping_counter}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
