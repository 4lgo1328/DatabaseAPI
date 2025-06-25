from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate, TelegramIDRequest, UserIDResponse
from app.crud.user_crud import (create_user, )
from typing import List

router = APIRouter()


@router.post("/create", response_model=UserRead)
async def create_user_route(user_data: UserCreate,
                      db: AsyncSession = Depends(get_db())):
    result = await create_user(db, user_data)
    return result

@router.post("/me", response_model=UserRead)
async def get_user_route(telegram_id: int,
                         db: AsyncSession = Depends(get_db())):
    pass
    # todo fill all the routes


# todo test the api functionality