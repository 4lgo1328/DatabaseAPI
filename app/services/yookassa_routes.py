from fastapi import APIRouter, HTTPException, Header

from app.core.security import verify_admin_token
from app.services.yookassa import create_yookassa_payment

router = APIRouter(prefix="/yookassa", tags=["YooKassa"])

@router.post("/create-payment")
async def create_payment(
    amount: float,
    user_telegram_id: int,
    return_url: str,
    x_auth_key: str = Header(alias="X-Auth-Key")
):
    auth_res = await verify_admin_token(x_auth_key)
    if auth_res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Invalid token")
    try:
        data = create_yookassa_payment(amount, user_telegram_id, return_url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
