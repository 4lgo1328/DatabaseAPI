from datetime import datetime
from typing import Sequence

from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.subscription import SubscriptionCreateByTGID


async def create_subscription(db: AsyncSession, data: SubscriptionCreateByTGID) -> Subscription:
    subscription = Subscription(**data.model_dump())
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription

async def get_active_subscription(db: AsyncSession, user_telegram_id: int) -> Subscription | None:
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.user_telegram_id == user_telegram_id,
            Subscription.end_date >= datetime.utcnow()
        )
        .order_by(desc(Subscription.start_date))
    )
    return result.scalar_one_or_none()


async def get_user_subscriptions(db: AsyncSession, user_telegram_id: int) -> Sequence[Subscription] | None:
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_telegram_id == user_telegram_id)
        .order_by(desc(Subscription.start_date))
    )
    return result.scalars().all()


async def delete_subscription(db: AsyncSession, telegram_id: int) -> bool:
    result = await db.execute(
        select(User)
        .where(User.telegram_id == telegram_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        return False

    await db.execute(
        delete(Subscription).where(Subscription.user_telegram_id == user.telegram_id) # type: ignore
    )
    await db.commit()
    return True
