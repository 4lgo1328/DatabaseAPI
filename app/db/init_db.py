# THIS FILE MUST BE RUNNED FIRST TIME BEFORE API USAGE. IT INITIALIZES DATABASE TABLES

import asyncio
from app.db.database import engine
from app.db.base_class import Base
from app.db.base import * # -----| DO NOT REMOVE THIS LINE |-----


async def init_models():
    async with engine.begin() as conn:
        print("Creating tables:", list(Base.metadata.tables.keys()))
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())