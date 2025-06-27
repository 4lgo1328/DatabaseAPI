from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

from app.models.enums import TaskStatus


class TaskCreate(BaseModel):
    client_id: int
    title: str
    description: Optional[str] = None
    assistant_id: Optional[int] = None


class TaskUpdate(BaseModel):
    UID: int
    title: Optional[str] = None
    description: Optional[str] = None
    assistant_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    completed_at: Optional[datetime] = None
    @field_validator("completed_at")
    @classmethod
    def remove_tz(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value.tzinfo:
            return value.replace(tzinfo=None)
        return value

class TaskRead(BaseModel):
    UID: int
    client_id: int
    assistant_id: Optional[int]
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    @field_validator("created_at", "updated_at", "completed_at")
    @classmethod
    def remove_tz(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value.tzinfo:
            return value.replace(tzinfo=None)
        return value



    class Config:
        from_attributes = True





class FileCreate(BaseModel):
    task_id: int
    uploader_telegram_id: int
    file_url: str


class FileRead(BaseModel):
    UID: int
    task_id: int
    uploader_telegram_id: int
    file_url: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def remove_tz(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value.tzinfo:
            return value.replace(tzinfo=None)
        return value

    class Config:
        from_attributes = True

class TaskUID(BaseModel):
    UID: int