from src.app.core.uow import UnitOfWork
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db_session import get_db_session


async def get_uow(
    db_session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[UnitOfWork, None]:
        async with UnitOfWork(db_session) as uow:
            yield uow