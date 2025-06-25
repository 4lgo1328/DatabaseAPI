from app.models.enums import TaskStatus
from app.db.base_class import Base


from sqlalchemy import Integer, String, Text, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.user import User


class Task(Base):
    __tablename__ = 'tasks'

    UID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id',
                   ondelete="CASCADE"),
        nullable=False
    )
    assistant_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.telegram_id',
                   ondelete="CASCADE"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped["TaskStatus"] = mapped_column(
        Enum("TaskStatus"),
        nullable=False,
        default=TaskStatus.new
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[client_id])


class File(Base):
    __tablename__ = 'files'

    UID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.UID'),
        nullable=False
    )
    uploader_telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id'),
        nullable=False
    )

    file_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    task: Mapped["Task"] = relationship("Task", foreign_keys=[task_id])
    uploader: Mapped["User"] = relationship("User", foreign_keys=[uploader_telegram_id])
