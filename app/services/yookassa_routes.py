from fastapi import APIRouter, HTTPException
from app.services.yookassa import create_yookassa_payment

router = APIRouter(prefix="/yookassa", tags=["YooKassa"])

@router.post("/create-payment")
async def create_payment(amount: float, user_telegram_id: int):
    try:
        payment_url = create_yookassa_payment(amount, user_telegram_id)
        return {"confirmation_url": payment_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))