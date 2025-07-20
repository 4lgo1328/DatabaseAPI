from sqlalchemy import (
    Integer, String, Enum
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.enums import UserRole
from app.db.base_class import Base

class StaffCode(Base):
    __tablename__ = 'staff_codes'

    UID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="UserRole"),
        nullable=False
    )
    code: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

