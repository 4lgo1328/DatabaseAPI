from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user_crud import (create_user,
                                get_user,
                                update_user,
                                get_all_users,
                                delete_user)
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/auth", response_model=UserRead)
async def auth_user_route(user_data: UserCreate,
                          db: AsyncSession = Depends(get_db())):
    result = await get_or_create_user(db, user_data)


@router.post("/create", response_model=UserRead)
async def create_user_route(user_data: UserCreate,
                            db: AsyncSession = Depends(get_db())):
    result = await create_user(db, user_data)
    return result

@router.get("/profile", response_model=UserRead)
async def get_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                         db: AsyncSession = Depends(get_db())):
    result = await get_user(db, telegram_id)
    return result

@router.put("/update", response_model=UserRead)
async def update_user_route(new_data: UserUpdate,
                            telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db())):
    result = await update_user(db, telegram_id, new_data)
    return result

@router.get("/all", response_model=List[UserRead])
async def get_all_users_route(db: AsyncSession = Depends(get_db())):
    return await get_all_users(db)


@router.get("/delete")
async def delete_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db())) -> bool:
    result = await delete_user(db, telegram_id)
    return result