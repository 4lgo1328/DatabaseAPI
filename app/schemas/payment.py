from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.models.enums import PaymentStatus


class PaymentCreate(BaseModel):
    user_telegram_id: int
    payment_txn_id: str
    amount: Decimal
    status: Optional[PaymentStatus] = PaymentStatus.pending


class PaymentUpdateByTxn(BaseModel):
    payment_txn_id: str
    new_status: PaymentStatus


class PaymentRead(BaseModel):
    UID: int
    payment_txn_id: str
    user_telegram_id: int

    amount: Decimal
    status: PaymentStatus

    payment_date: datetime

    class Config:
        from_attributes = True