from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from src.app.core.database import DatabaseConnection
from src.app.dependencies.database import get_database_connection
from fastapi import Depends


async def get_db_session(
    db_connection: DatabaseConnection = Depends(get_database_connection)  # ← Здесь Request автоматически передается
) -> AsyncGenerator[AsyncSession, None]:
    session_session = await db_connection.get_async_session()
    async with session_session() as db_session:
        yield db_session