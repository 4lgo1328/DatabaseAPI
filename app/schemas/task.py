from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.enums import TaskStatus


class TaskCreate(BaseModel):
    client_id: int
    title: str
    description: Optional[str] = None
    assistant_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assistant_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    completed_at: Optional[datetime] = None


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

    class Config:
        from_attributes = True

class TaskUID(BaseModel):
    UID: int