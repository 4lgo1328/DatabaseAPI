from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import PaymentStatus, PlanType
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


async def create_payment(db: AsyncSession, data: PaymentCreate) -> Payment | None:
    if data.plan_hrs not in [2,5,8]:
        return None
    payment = Payment(**data.model_dump())
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_payment_by_txn_id(db: AsyncSession, payment_txn_id: str) -> Payment | None:
    result = await db.execute(
        select(Payment)
        .where(Payment.payment_txn_id == payment_txn_id) # type: ignore
    )
    return result.scalar_one_or_none()

async def get_payments_by_user(db: AsyncSession, user_telegram_id: int) -> Sequence[Payment] | None:
    result = await db.execute(
        select(Payment)
        .where(Payment.user_telegram_id==user_telegram_id) # type: ignore
        .order_by(desc(Payment.payment_date))
    )
    return result.scalars().all()

async def update_payment_status(db: AsyncSession, payment_txn_id: str, new_status: PaymentStatus):
    payment = await db.get(Payment, payment_txn_id)
    if not payment:
        return None

    payment.status = new_status
    await db.commit()
    await db.refresh(payment)
    return payment

async def update_payment_plan(db: AsyncSession, payment_txn_id: str, new_plan: PlanType):
    payment = await db.get(Payment, payment_txn_id)
    if payment is None:
        return None
    payment.plan = new_plan
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_all_payments(db: AsyncSession) -> Sequence[Payment]:
    result = await db.execute(
        select(Payment)
    )
    return result.scalars().all()


async def delete_payment_by_txn_id(db: AsyncSession, payment_txn_id: str) -> type[Payment] | None:
    payment = await db.get(Payment, payment_txn_id)
    if payment is None:
        return None

    await db.delete(payment)
    await db.commit()
    return payment