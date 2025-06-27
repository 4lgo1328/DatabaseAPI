from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException

from app.crud.task_crud import *
from app.schemas.task import TaskRead
from app.db.database import get_db
from app.core.security import verify_token
from app.crud.subscription_crud import get_active_subscription

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=TaskRead)
async def create_task_route(data: TaskCreate,
                            db: AsyncSession = Depends(get_db),
                            token: str = Header(alias="X-Auth-Token")):

    if not get_active_subscription(db, data.client_id):
        raise HTTPException(status_code=403, detail="No active subscription")

    res = await verify_token(db, data.client_id, token)

    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await create_task(db, data)
    return result

@router.get("/by_uid", response_model=TaskRead)
async def get_task_by_id_route(UID: int = Header(alias="Task-UID"),
                               db: AsyncSession = Depends(get_db),
                               token: str = Header(alias="X-Auth-Token")):
    if not UID:
        raise HTTPException(status_code=401, detail="Task UID must be passed")

    task: Task | None = await get_task_by_id(db, UID)

    if not task:
        return None

    res = await verify_token(db, task.client_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    return task

@router.get("/user", response_model=List[TaskRead])
async def get_tasks_by_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                  db: AsyncSession = Depends(get_db),
                                  token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_user_tasks(db, telegram_id)
    return result

@router.put("/update", response_model=TaskRead)
async def update_task_route(data: TaskUpdate,
                            db: AsyncSession = Depends(get_db),
                            token: str = Header(alias="X-Auth-Token")):
    if not data.UID:
        raise HTTPException(status_code=401, detail="Task UID must be passed")

    task: Task | None = await get_task_by_id(db, data.UID)

    if not task: raise HTTPException(status_code=404, detail="Task not found")

    res = await verify_token(db, task.client_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await update_task(db, data)
    return result

