from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from app.models.enums import UserRole


class UserCreate(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    role: Optional[UserRole] = UserRole.client

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    role: Optional[UserRole] = None
    assigned_manager_telegram_id: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(BaseModel):
    UID: int
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    role: UserRole
    created_at: datetime
    is_active: bool
    assigned_manager_telegram_id: Optional[int] = None

    class Config:
        from_attributes = True
