from typing import AsyncGenerator
from app.core.config import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import URL

conn_url = URL.create(
    drivername=config.db_drivername,
    password=config.db_password,
    username=config.db_username,
    host=config.db_host,
    port=config.db_port,
    database=config.db_database,
)

engine = create_async_engine(url=conn_url)

AsynSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsynSessionLocal() as session:
        yield session
