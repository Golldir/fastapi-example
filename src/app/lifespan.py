from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import TypedDict
import asyncio
from fastapi import FastAPI, Depends
from src.app.core.database import DatabaseConnection
from src.app.core.redis import RedisConnection
from src.app.core.config import settings
class AppState(TypedDict):
    db: DatabaseConnection
    redis: RedisConnection


@asynccontextmanager
async def lifespan(
    app: FastAPI
) -> AsyncIterator[AppState]:
    database = DatabaseConnection(db_url=str(settings.db_dsn))
    await database.open_connection()
    await database.check_connection()

    redis = RedisConnection(redis_url=str(settings.redis_dsn))
    await redis.open_connection()
    await redis.check_connection()

    app.state.database: DatabaseConnection = database
    app.state.redis: RedisConnection = redis

    yield 
    # Закрытие (выполняется после yield)
    await database.close_connection()
    await redis.close_connection()