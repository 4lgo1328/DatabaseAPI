from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_admin_token
from app.db.database import get_db
from app.schemas.assistant import AssistantStatsCreate, AssistantStatsRead
from app.crud import assistant_crud

router = APIRouter(prefix="/assistant-statistics", tags=["AssistantStatistics"])

@router.post("/stats/", response_model=AssistantStatsRead)
async def create_or_update_assistant_stats(
    stats: AssistantStatsCreate,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(...)
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return await assistant_crud.create_or_update_assistant_stats(db, stats)


@router.get("/stats/{telegram_id}", response_model=AssistantStatsRead)
async def get_assistant_stats(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(...)
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    stats = await assistant_crud.get_assistant_stats_by_telegram_id(db, telegram_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


@router.post("/stats/update/{telegram_id}", response_model=AssistantStatsRead)
async def calculate_and_update_assistant_stats(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
    x_auth_key: str = Header(...)
):
    auth = await verify_admin_token(x_auth_key)
    if auth["status"] != "OK":
        raise HTTPException(status_code=403, detail="Invalid admin token")
    stats = await assistant_crud.calculate_and_update_task_stats(db, telegram_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No completed tasks or assistant not found")
    return stats
