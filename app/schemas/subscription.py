from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.enums import PlanType


class SubscriptionCreateByTGID(BaseModel):
    user_telegram_id: int
    plan: PlanType
    start_date: datetime
    end_date: datetime
    payment_txn_id: str

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def remove_tz(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            value = datetime.fromisoformat(value)
        return value.replace(tzinfo=None) if value.tzinfo else value

class SubscriptionRead(BaseModel):
    UID: int
    user_telegram_id: int
    plan: PlanType
    start_date: datetime
    end_date: datetime
    created_at: datetime
    payment_txn_id: str

    class Config:
        from_attributes = True