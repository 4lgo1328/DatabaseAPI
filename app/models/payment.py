from datetime import datetime

from sqlalchemy import (
    Integer, String, Enum, DECIMAL, func, DateTime, Sequence
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.enums import *
from app.db.base_class import Base

uid_seq = Sequence("payment_uid_seq")

class Payment(Base):
    __tablename__ = 'payments'

    UID: Mapped[int] = mapped_column(
        Integer,
        uid_seq,
        server_default=uid_seq.next_value(),
        unique=True,
        nullable=False
    )
    user_telegram_id: Mapped[int] = mapped_column(
        Integer
    )
    payment_txn_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        primary_key=True,
        nullable=False
    )
    amount: Mapped[float] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    plan: Mapped[PlanType] = mapped_column(
        Enum(PlanType, name="PlanType"),
        nullable=False
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="PaymentStatus"),
        default=PaymentStatus.pending
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
