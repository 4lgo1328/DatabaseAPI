from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings
from base_class import Base


engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker( # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session