from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException

from app.crud.subscription_crud import *
from app.db.database import get_db
from app.schemas.subscription import SubscriptionRead

from app.core.security import verify_token, verify_admin_token

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/all", response_model=List[SubscriptionRead])
async def get_all_subscriptions_route(db: AsyncSession = Depends(get_db),
                                token: str = Header(alias="X-Auth-Token")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")
    result = await get_all_subscriptions(db)
    return result
            
@router.post("/create", response_model=SubscriptionRead)
async def create_subscription_route(data: SubscriptionCreateByTGID,
                                    db: AsyncSession = Depends(get_db),
                                    token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, data.user_telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await create_subscription(db, data)
    return result

@router.get("/active", response_model=SubscriptionRead)
async def get_active_subscription_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                        db: AsyncSession = Depends(get_db),
                                        token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_active_subscription(db, telegram_id)
    if not result: raise HTTPException(status_code=404, detail="No active subscription found")
    return result

@router.get("/get", response_model=List[SubscriptionRead])
async def get_subscription_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                 db: AsyncSession = Depends(get_db),
                                 token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_user_subscriptions(db, telegram_id)
    if not result: raise HTTPException(status_code=404, detail="No subscriptions found")
    return result

@router.delete("/delete", response_model=bool)
async def delete_subscription_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                    db: AsyncSession = Depends(get_db),
                                    token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await delete_subscription(db, telegram_id)
    return result
