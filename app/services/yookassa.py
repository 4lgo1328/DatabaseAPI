from yookassa import Payment, Configuration
from app.core.settings import settings
import uuid
import os


Configuration.account_id = settings.admin_secret_key
Configuration.secret_key = settings.yookassa_api_key


def create_yookassa_payment(amount: float, telegram_id: int) -> str:
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://rentassistant.ru/payment-success"
        },
        "capture": True,
        "description": f"Оплата от пользователя {telegram_id}"
    }, uuid.uuid4())

    return payment.confirmation.confirmation_url
