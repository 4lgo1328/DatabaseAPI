from fastapi import APIRouter, Depends, Header

from app.crud.subscription_crud import *
from app.db.database import get_db
from app.schemas.subscription import SubscriptionRead

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/create", response_model=SubscriptionRead)
async def create_subscription_route(data: SubscriptionCreateByTGID,
                                    db: AsyncSession = Depends(get_db())):
    result = await create_subscription(db, data)
    return result

@router.get("/active", response_model=SubscriptionRead)
async def get_active_subscription_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                        db: AsyncSession = Depends(get_db())):
    result = await get_active_subscription(db, telegram_id)
    return result

@router.get("/get", response_model=SubscriptionRead)
async def get_active_subscription_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                        db: AsyncSession = Depends(get_db())):
    result = await get_user_subscriptions(db, telegram_id)
    return result

@router.delete("/delete", response_model=bool)
async def delete_subscription_route(telegram_id: int = Header(alias="X-Telegram_ID"),
                                    db: AsyncSession = Depends(get_db())):
    result = await delete_subscription(db, telegram_id)
    return result