from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.models.enums import PaymentStatus, PlanType


class PaymentCreate(BaseModel):
    user_telegram_id: int
    payment_txn_id: str
    plan: PlanType
    amount: Decimal
    status: Optional[PaymentStatus] = PaymentStatus.pending


class PaymentUpdateStatusByTxn(BaseModel):
    payment_txn_id: str
    new_status: PaymentStatus

class PaymentUpdatePlanByTxn(BaseModel):
    payment_txn_id: str
    new_plan: PlanType

class PaymentTxn(BaseModel):
    payment_txn_id: str


class PaymentRead(BaseModel):
    UID: int
    payment_txn_id: str
    user_telegram_id: int

    amount: Decimal
    status: PaymentStatus
    plan: PlanType


    payment_date: datetime

    class Config:
        from_attributes = True