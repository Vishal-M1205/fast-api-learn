from db_engine import conn_url
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
import asyncio

#! the ext - extension contains new features developed


engine = create_async_engine(conn_url, pool_size=3)
#! same config of QueuePool


async def main():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print(result.scalar())
    finally:
        await engine.dispose()  #! Used to clean the resources


asyncio.run(main())


# * async with and await cannot be executed alone need to wrap it in a function


# !!! The above code wont run because it need a different event loop , not in the windows
#! ProactorEventLoop in win32 , but it needs SelectorEventLoop
