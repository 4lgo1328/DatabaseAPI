from datetime import datetime

from sqlalchemy import (
    Integer, Enum, ForeignKey, TIMESTAMP, func, DateTime, String, Sequence
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.enums import *

from app.db.base_class import Base
from app.models.user import User

uid_seq = Sequence("subscription_uid_seq")

class Subscription(Base):
    __tablename__ = 'subscriptions'

    UID: Mapped[int] = mapped_column(
        Integer,
        uid_seq,
        server_default=uid_seq.next_value(),
        unique=True,
        nullable=False
    )
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id',
                   ondelete="CASCADE"),
        nullable=False
    )
    plan: Mapped["PlanType"] = mapped_column(
        Enum(PlanType, name="PlanType"),
        nullable=False
    )
    plan_hrs: Mapped["PlanTime"] = mapped_column(
        Enum(PlanTime, name="PlanTime"),
        nullable=False
    )
    remaining_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=func.now()
    )
    end_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    payment_txn_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True
    )

    user: Mapped["User"] = relationship("User")

