from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, File
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task import FileCreate

async def create_task(db: AsyncSession, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task_by_id(db: AsyncSession, task_UID: int) -> Task | None:
    result = await db.execute(select(Task).where(Task.UID == task_UID))
    return result.scalar_one_or_none()


async def get_user_tasks(db: AsyncSession, tg_id: int) -> Sequence[Task] | None:
    result = await db.execute(
        select(Task)
        .where(Task.client_id == tg_id)
    )
    return result.scalars().all()


async def update_task(db: AsyncSession, data: TaskUpdate) -> Task | None:
    task = await get_task_by_id(db, data.UID)

    if not task:
        return None

    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


async def upload_file(db: AsyncSession, data: FileCreate) -> File:
    file = File(**data.model_dump())
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file


async def get_files_by_task_id(db: AsyncSession, task_id: int) -> Sequence[File] | None:
    result = await db.execute(
        select(File)
        .where(File.task_id == task_id)
    )
    return result.scalars().all()