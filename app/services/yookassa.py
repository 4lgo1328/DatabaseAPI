from yookassa import Payment, Configuration
from yookassa.domain.response import PaymentResponse

from app.core.settings import settings
import uuid

Configuration.account_id = settings.shop_id
Configuration.secret_key = settings.yookassa_api_key

def create_yookassa_payment(
    amount: float,
    telegram_id: int,
    return_url: str
) -> dict[str, str]:
    payment: PaymentResponse = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": f"Оплата от пользователя {telegram_id}"
    }, uuid.uuid4())

    return {"confirmation_url": payment.confirmation.confirmation_url, "transaction_id": payment.id}
