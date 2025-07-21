from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import alias
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserGetOrCreate, PendingUserRead
from app.crud.user_crud import (create_user,
                                get_user,
                                update_user,
                                get_all_users,
                                delete_user, get_or_create_user, get_or_create_pending, increment_notification)
from typing import List
from app.core.security import verify_token, verify_admin_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/auth", response_model=UserRead)
async def auth_user_route(user_data: UserCreate,
                          db: AsyncSession = Depends(get_db)):
    data = UserGetOrCreate(**user_data.model_dump())
    result = await get_or_create_user(db, data)
    return result


@router.post("/create", response_model=UserRead)
async def create_user_route(user_data: UserCreate,
                            db: AsyncSession = Depends(get_db)):
    result = await create_user(db, user_data)
    return result

@router.get("/profile", response_model=UserRead)
async def get_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                         db: AsyncSession = Depends(get_db),
                         token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_user(db, telegram_id)
    return result

@router.put("/update", response_model=UserRead)
async def update_user_route(new_data: UserUpdate,
                            telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db),
                            token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await update_user(db, telegram_id, new_data)
    return result

@router.get("/all", response_model=List[UserRead])
async def get_all_users_route(db: AsyncSession = Depends(get_db),
                              token: str = Header(alias="X-Auth-Token")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    return await get_all_users(db)


@router.get("/delete")
async def delete_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db),
                            token: str = Header(alias="X-Auth-Token")) -> bool:
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await delete_user(db, telegram_id)
    return result

@router.post("/get-or-create-pending", response_model=PendingUserRead)
async def get_or_create_pending_route(db: AsyncSession = Depends(get_db),
                                      token: str = Header(alias="X-Auth-Token"),
                                      telegram_id: int = Header(alias="X-Telegram-ID")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_or_create_pending(db, telegram_id)
    return result


@router.post("/increment-notification", response_model=PendingUserRead)
async def increment_notification_route(db: AsyncSession = Depends(get_db),
                                      token: str = Header(alias="X-Auth-Token"),
                                      telegram_id: int = Header(alias="X-Telegram-ID")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await increment_notification(db, telegram_id)
    return result

@router.get("/get-all-pending", response_model=List[PendingUserRead])
async def get_all_pending(db: AsyncSession = Depends(get_db),
                          token: str = Header(alias="X-Auth-Token")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")
    result = await get_all_pending(db)
    return result