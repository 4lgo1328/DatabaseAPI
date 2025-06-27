from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserGetOrCreate
from app.crud.user_crud import (create_user,
                                get_user,
                                update_user,
                                get_all_users,
                                delete_user, get_or_create_user)
from typing import List
from app.core.security import verify_token, verify_admin_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/auth", response_model=UserRead)
async def auth_user_route(user_data: UserCreate,
                          db: AsyncSession = Depends(get_db())):
    data = UserGetOrCreate(**user_data.model_dump())
    result = await get_or_create_user(db, data)
    return result


@router.post("/create", response_model=UserRead)
async def create_user_route(user_data: UserCreate,
                            db: AsyncSession = Depends(get_db())):
    result = await create_user(db, user_data)
    return result

@router.get("/profile", response_model=UserRead)
async def get_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                         db: AsyncSession = Depends(get_db()),
                         token: str = Header(alias="X-Auth-Token")):

    if not await verify_token(telegram_id=telegram_id,
                              public_user_token=token):
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_user(db, telegram_id)
    return result

@router.put("/update", response_model=UserRead)
async def update_user_route(new_data: UserUpdate,
                            telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db()),
                            token: str = Header(alias="X-Auth-Token")):

    if not await verify_token(telegram_id=telegram_id,
                              public_user_token=token):
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await update_user(db, telegram_id, new_data)
    return result

@router.get("/all", response_model=List[UserRead])
async def get_all_users_route(db: AsyncSession = Depends(get_db()),
                              token: str = Header(alias="X-Auth-Token")):

    if not await verify_admin_token(token):
        raise HTTPException(status_code=403, detail="Token is invalid")

    return await get_all_users(db)


@router.get("/delete")
async def delete_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                            db: AsyncSession = Depends(get_db()),
                            token: str = Header(alias="X-Auth-Token")) -> bool:

    if not await verify_token(telegram_id=telegram_id,
                              public_user_token=token):
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await delete_user(db, telegram_id)
    return result