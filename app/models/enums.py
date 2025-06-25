import enum


class UserRole(str, enum.Enum):
    """
    Enum representing role of a user in terms of service
    """
    client = 'client'
    assistant = 'assistant'
    manager = 'manager'

class PlanType(str, enum.Enum):
    """
    Enum representing tariff type
    """
    light = 'light'
    business = 'business'
    extra = 'extra'

class SubscriptionStatus(str, enum.Enum):
    """
    Enum representing statud of user subscription
    """
    active = 'active'
    expired = 'expired'
    cancelled = 'cancelled'
    pending_payment = 'pending_payment'

class PaymentStatus(str, enum.Enum):
    """
    Enum representing status of a payment
    """
    canceled = 'canceled'
    succeeded = 'succeeded'
    failed = 'failed'
    pending = 'pending'
    refunded = 'refunded'

class TaskStatus(str, enum.Enum):
    """
    Enum representing status of a task given by user to an assistant
    """
    new = 'new'
    in_progress = 'in_progress'
    completed = 'completed'
    needs_revision = 'needs_revision'