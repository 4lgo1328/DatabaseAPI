from sqlalchemy import Column, Integer, BigInteger, Float, ForeignKey
from app.db.base_class import Base


class AssistantStatistics(Base):
    __tablename__ = "assistant_statistics"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    clients = Column(Integer, nullable=False)
    tasks_completed = Column(Integer, nullable=False)
    avg_completion_time = Column(Integer, default=0)
    task_completion_percent = Column(Float, default=0.0)
    time_overall = Column(Integer, default=0)
    time_occupied = Column(Integer, default=0)
