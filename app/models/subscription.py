from datetime import datetime

from sqlalchemy import (
    Integer, Enum, ForeignKey, TIMESTAMP, func, DateTime, String
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.enums import *

from app.db.base_class import Base
from app.models.user import User


class Subscription(Base):
    __tablename__ = 'subscriptions'

    UID: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True
    )
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id',
                   ondelete="CASCADE"),
        nullable=False
    )
    plan: Mapped["PlanType"] = mapped_column(
        Enum(PlanType),
        nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
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

