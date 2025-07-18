from sqlalchemy import Integer, BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.models.user import User


class AssistantStatistics(Base):
    __tablename__ = "assistant_statistics"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id",
                   ondelete="CASCADE"),
        primary_key=True,
        index=True
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="assistant_statistics"
    )

    clients_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tasks_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_completion_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    task_completion_percent: Mapped[float] = mapped_column(Float, default=0.0)
    time_overall_minutes: Mapped[int] = mapped_column(Integer, default=0)
    time_occupied_minutes: Mapped[int] = mapped_column(Integer, default=0)
    kudos: Mapped[int] = mapped_column(Integer, default=0)
