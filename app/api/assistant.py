from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_admin_token
from app.crud.assistant_crud import change_clients_count, kudos_assistant, increment_assistant_task, \
    add_client_to_assistant, change_occupied_time, change_overall_minutes
from app.db.database import get_db
from app.schemas.assistant import AssistantStatsCreate, AssistantStatsRead
from app.crud import assistant_crud

router = APIRouter(prefix="/assistant-statistics", tags=["AssistantStatistics"])

@router.post("/stats/", response_model=AssistantStatsRead)
async def create_or_update_assistant_stats(
    stats: AssistantStatsCreate,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(alias="X-Auth-Key")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return await assistant_crud.create_or_update_assistant_stats(db, stats)


@router.get("/stats/{telegram_id}", response_model=AssistantStatsRead)
async def get_assistant_stats(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(alias="X-Auth-Key")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    stats = await assistant_crud.get_assistant_stats_by_telegram_id(db, telegram_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats

@router.patch("/change-clients-count")
async def change_assistant_clients_count(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID"),
    new_clients_number: int = Header(alias="X-Clients-Number")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    changes = await change_clients_count(db, telegram_id, new_clients_number)
    if not changes:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return changes

@router.patch("/kudos")
async def kudos_assistant_endpoint(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    res = await kudos_assistant(db, telegram_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return res

@router.patch("/add-task")
async def add_assistant_task(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    res = await increment_assistant_task(db, telegram_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return res

@router.patch("/add-client")
async def add_assistant_client(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    res = await add_client_to_assistant(db, telegram_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return res

@router.patch("/change-occupied-time")
async def change_time_occipied(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID"),
    new_occupied_time: int = Header(alias="New-Occupied-Time")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    res = await change_occupied_time(db, telegram_id, new_occupied_time)
    if res is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return res


@router.patch("/change-overall-time")
async def change_time_overall(
    x_auth_key: str = Header(alias="X-Auth-Key"),
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Header(alias="X-Assistant-ID"),
    new_overall_time: int = Header(alias="New-Overall-Time")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    res = await change_overall_minutes(db, telegram_id, new_overall_time)
    if res is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return res

@router.post("/stats/update/{telegram_id}", response_model=AssistantStatsRead)
async def calculate_and_update_assistant_stats(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(alias="X-Auth-Key")
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    stats = await assistant_crud.calculate_and_update_task_stats(db, telegram_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No completed tasks or assistant not found")
    return stats
