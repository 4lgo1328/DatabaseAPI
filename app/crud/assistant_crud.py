from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.task import Task
from app.models.assistant import AssistantStatistics
from app.schemas.assistant import AssistantStatsCreate, AssistantStatsUpdate


async def create_or_update_assistant_stats(db: AsyncSession, data: AssistantStatsCreate) -> AssistantStatistics:
    stats = await db.get(AssistantStatistics, data.telegram_id)
    if stats:
        for field, value in data.model_dump(exclude_unset=True, exclude_defaults=True).items():
            setattr(stats, field, value)
    else:
        stats = AssistantStatistics(**data.model_dump())
        db.add(stats)

    await db.commit()
    await db.refresh(stats)
    return stats


async def get_assistant_stats_by_telegram_id(db: AsyncSession, telegram_id: int) -> AssistantStatistics | None:
    return await db.get(AssistantStatistics, telegram_id)


async def calculate_and_update_task_stats(db: AsyncSession, telegram_id: int) -> AssistantStatistics | None:
    user = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user_found: User = user.scalar_one_or_none()
    if not user_found:
        return None

    result = await db.execute(
        select(Task)
        .where(Task.assistant_id == user_found.telegram_id, Task.status == "completed")
    )
    tasks = result.scalars().all()

    if not tasks:
        return None

    completed_count = len(tasks)
    durations = [
        (task.completed_at - task.created_at).total_seconds() / 60
        for task in tasks
        if task.completed_at and task.created_at
    ]
    avg_time = sum(durations) / len(durations) if durations else None

    stats = await db.get(AssistantStatistics, telegram_id)
    if not stats:
        stats = AssistantStatistics(telegram_id=telegram_id)
        db.add(stats)

    stats.tasks_completed = completed_count
    stats.avg_completion_time = avg_time

    await db.commit()
    await db.refresh(stats)
    return stats
