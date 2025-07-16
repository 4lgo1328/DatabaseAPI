from fastapi import APIRouter, HTTPException
from app.services.yookassa import create_yookassa_payment

router = APIRouter(prefix="/yookassa", tags=["YooKassa"])

@router.post("/create-payment")
async def create_payment(
    amount: float,
    user_telegram_id: int,
    return_url: str
):
    try:
        confirmation_url = create_yookassa_payment(amount, user_telegram_id, return_url)
        return {"confirmation_url": confirmation_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
