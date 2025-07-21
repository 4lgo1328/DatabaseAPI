from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from app.models.enums import UserRole

class UserGetOrCreate(BaseModel):
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    phone_number: Optional[str]  # "+79007776655"
    role: Optional[UserRole] = UserRole.client

class UserCreate(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    phone_number: str  # "+79007776655"
    role: Optional[UserRole] = UserRole.client

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    role: Optional[UserRole] = None
    assigned_manager_telegram_id: Optional[int] = None
    is_active: Optional[bool] = None
    has_free_task: Optional[bool] = None

class UserRead(BaseModel):
    UID: int
    telegram_id: int
    username: str
    first_name: str
    role: UserRole
    created_at: datetime
    phone_number: str # "+79007776655"
    is_active: bool
    personal_public_token: str
    has_free_task: bool
    assigned_manager_telegram_id: Optional[int] = None

    class Config:
        from_attributes = True

class PendingUserRead(BaseModel):
    telegram_id: int
    joined_at: datetime
    reminders_sent: int

    class Config:
        orm_mode = True