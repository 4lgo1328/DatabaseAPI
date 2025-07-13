from pydantic import BaseModel
from typing import Optional


class AssistantStatsCreate(BaseModel):
    telegram_id: int
    tasks_completed: int = 0
    avg_completion_time: Optional[float] = 0.0
    task_completion_percent: Optional[float] = 0.0
    time_overall: Optional[int] = 0
    time_occupied: Optional[int] = 0


class AssistantStatsRead(BaseModel):
    telegram_id: int
    tasks_completed: int
    avg_completion_time: Optional[float] = 0.0
    task_completion_percent: Optional[float] = 0.0
    time_overall: Optional[int] = 0
    time_occupied: Optional[int] = 0

    class Config:
        from_attributes = True
