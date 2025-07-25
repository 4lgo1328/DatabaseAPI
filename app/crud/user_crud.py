from typing import Sequence
import logging

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, PendingUser
from app.schemas.user import UserCreate, UserGetOrCreate, UserUpdate
from app.misc.generator import generate_token


async def get_or_create_user(db: AsyncSession, user_data: UserGetOrCreate):
    user: User | None = await db.get(User, user_data.telegram_id)
    if user is None:
        return await create_user(db, UserCreate(**user_data.model_dump()))
    return user

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    new_user: User = User(**user_data.model_dump(),
                          personal_public_token=generate_token(user_data.telegram_id))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id) )
    user: User | None = result.scalar_one_or_none()
    return user

async def update_user(
        db: AsyncSession, telegram_id: int, user_update: UserUpdate
) -> User | None:

    result = await db.execute(select(User).where(User.telegram_id==telegram_id))
    user: User | None = result.scalar_one_or_none()
    if user is None:
        return None

    for field, value in user_update.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    logging.log(logging.INFO, user)
    return user


async def get_all_users(db: AsyncSession) -> Sequence[User]:
    result = await db.execute(
        select(User)
    )
    return result.scalars().all()


async def delete_user(db: AsyncSession, telegram_id: int) -> bool:
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return False


    await db.execute(
        delete(User).where(User.telegram_id == user.telegram_id)
    )
    await db.commit()
    return True


async def add_to_pending(db: AsyncSession, telegram_id: int) -> PendingUser:
    user: PendingUser = PendingUser(telegram_id=telegram_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def increment_notification(db: AsyncSession, telegram_id: int) -> PendingUser | None:
    res = await db.execute(select(PendingUser).where(PendingUser.telegram_id==telegram_id))
    user: PendingUser | None = res.scalar_one_or_none()
    if user is None:
        return None
    user.reminders_sent += 1
    await db.commit()
    await db.refresh(user)
    return user

async def delete_pending_user(db: AsyncSession, telegram_id: int) -> bool:
    result = await db.execute(
        select(PendingUser).where(PendingUser.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return False

    await db.execute(delete(PendingUser).where(PendingUser.telegram_id==telegram_id))
    await db.commit()
    return True

async def get_or_create_pending(db: AsyncSession, telegram_id: int) -> PendingUser:
    result = await db.execute(
        select(PendingUser).where(PendingUser.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    user: PendingUser = PendingUser(telegram_id=telegram_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_all_pending(db: AsyncSession) -> Sequence[PendingUser]:
    result = await db.execute(
        select(PendingUser)
    )
    pus = result.scalars().all()
    return pus