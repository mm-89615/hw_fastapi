from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import PG_DSN
from models.base import Base

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
