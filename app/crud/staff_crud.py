import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.staff import StaffCode


async def create_code(db: AsyncSession, role: UserRole) -> str:
    code = str(uuid.uuid4())
    new_obj: StaffCode = StaffCode(
        role=role,
        code=code
    )
    db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return code

async def issue_code(db: AsyncSession, code: str) -> str | None:
    res = await db.execute(select(StaffCode).where(StaffCode.code==code))
    staff_code: StaffCode | None = res.scalar_one_or_none()
    if staff_code is None:
        return None
    role: UserRole = staff_code.role
    await db.execute(delete(StaffCode).where(StaffCode.code==code))
    await db.commit()
    return role.value