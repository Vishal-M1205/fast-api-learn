from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import URL

conn_url = URL.create(
    drivername="postgresql+asyncpg",
    password="CG-vak123",
    username="postgres",
    host="localhost",
    port=5432,
    database="security_practice",
)

engine = create_async_engine(url=conn_url)

AsynSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsynSessionLocal() as session:
        yield session
