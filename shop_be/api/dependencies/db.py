from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from shop_be.conf.db import async_session


async def get_db_session() -> AsyncGenerator['AsyncSession', None]:
    """Dependency to get database session"""
    async with async_session() as session:
        yield session
