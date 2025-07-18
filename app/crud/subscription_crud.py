from datetime import datetime
from typing import Sequence

from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import PlanType, PlanTime
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.subscription import SubscriptionCreateByTGID

async def get_all_subscriptions(db: AsyncSession) -> Sequence[Subscription] | None:
    result = await db.execute(
        select(Subscription)
    )
    return result.scalars().all()

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

async def update_subscription_plan(db: AsyncSession, user_telegram_id: int, new_plan: PlanType) -> Subscription | None:
    result = await db.execute(select(Subscription).where(Subscription.user_telegram_id == user_telegram_id))
    user: User | None = result.scalar_one_or_none()
    if user is None:
        return None
    subscription: Subscription | None = await get_active_subscription(db, user_telegram_id)
    if subscription is None:
        return None
    subscription.plan = new_plan
    await db.commit()
    await db.refresh(Subscription)
    return subscription

async def update_subscription_plan_hrs(db: AsyncSession, user_telegram_id: int, new_plan_hrs: PlanTime) -> Subscription | None:
    result = await db.execute(select(Subscription).where(Subscription.user_telegram_id == user_telegram_id))
    user: User | None = result.scalar_one_or_none()
    if user is None:
        return None
    subscription: Subscription | None = await get_active_subscription(db, user_telegram_id)
    if subscription is None:
        return None
    subscription.plan_hrs = new_plan_hrs
    await db.commit()
    await db.refresh(Subscription)
    return subscription

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
