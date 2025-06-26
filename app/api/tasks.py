from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException

from app.crud.task_crud import *
from app.schemas.task import TaskRead, TaskUID
from app.db.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=TaskRead)
async def create_task_route(data: TaskCreate,
                            db: AsyncSession = Depends(get_db())):
    result = await create_task(db, data)
    return result

@router.get("/by_uid", response_model=TaskRead)
async def get_task_by_id_route(data: TaskUID,
                               db: AsyncSession = Depends(get_db())):
    if not data.UID:
        raise HTTPException(status_code=401, detail="Telegram id must be passed")
    result = await get_task_by_id(db, data.UID)
    return result

@router.get("/user", response_model=List[TaskRead])
async def get_tasks_by_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                  db: AsyncSession = Depends(get_db())):
    result = await get_user_tasks(db, telegram_id)
    return result
@router.put("/update", response_model=TaskRead)
async def update_task_route(data: TaskUpdate,
                            db: AsyncSession = Depends(get_db())):
    result = await update_task(db, data)

