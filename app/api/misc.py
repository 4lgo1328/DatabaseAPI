from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.payment_crud import update_payment_status
from app.crud.subscription_crud import create_subscription

from app.models.enums import PaymentStatus
from app.models.subscription import Subscription

from app.schemas.subscription import SubscriptionRead, SubscriptionCreateByTGID

from app.db.database import get_db

from app.core.security import verify_admin_token


router = APIRouter(prefix="misc", tags=["Misc"])

@router.get("/confirm subscription", response_model=SubscriptionRead)
async def activate_subscription(data: SubscriptionCreateByTGID,
                                db: AsyncSession = Depends(get_db()),
                                token: str = Header(alias="X-Auth-Token")):
    if not(await verify_admin_token(token)):
        raise HTTPException(status_code=403, detail="Token is invalid")

    subscription: Subscription = await create_subscription(db, data)

    await update_payment_status(db, subscription.payment_txn_id, PaymentStatus.succeeded)

    return subscription



