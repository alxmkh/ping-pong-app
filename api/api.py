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
        return {"pong": current_count_value.ping_counter}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get('/health-db', tags=['health_checks'])
async def get_database_health_check(db: Session = Depends(get_db)) -> dict[str] | Exception:
    try:
        health_check_result = crud.database_health_check(db)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    if health_check_result[0] == 'OK':
        return {"check_database_connection": health_check_result[0]}
    else:
        raise HTTPException(status_code=503, detail='Database unavailable')


@router.get('/health-app', tags=['health_checks'])
async def get_app_health_check() -> dict:
    return {"check_app_connection": "OK"}
