from pydantic import BaseModel
from typing import Optional


class AssistantStatsCreate(BaseModel):
    telegram_id: int
    clients_count: int = 0
    tasks_completed: int = 0
    avg_completion_time_minutes: Optional[float] = 0.0
    task_completion_percent: Optional[float] = 0.0
    time_overall_minutes: Optional[int] = 0
    time_occupied_minutes: Optional[int] = 0


class AssistantStatsRead(BaseModel):
    telegram_id: int
    clients_count: int
    tasks_completed: int
    avg_completion_time_minutes: Optional[float] = 0.0
    task_completion_percent: Optional[float] = 0.0
    time_overall_minutes: Optional[int] = 0
    time_occupied_minutes: Optional[int] = 0

    class Config:
        from_attributes = True



class AssistantStatsUpdate(BaseModel):
    telegram_id: int
    clients_count: Optional[int]
    tasks_completed: Optional[int]
    avg_completion_time_minutes: Optional[float]
    task_completion_percent: Optional[float]
    time_overall_minutes: Optional[int]
    time_occupied_minutes: Optional[int]