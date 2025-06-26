from sqlalchemy import (
    Integer, String, BigInteger, Enum, Boolean, func, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base_class import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = 'users'

    UID: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole,
             name="UserRole"
             ),
        nullable=False,
        default=UserRole.client
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    assigned_manager_telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True
    )
    personal_public_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False #todo
    )
