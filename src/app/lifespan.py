from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import TypedDict

from fastapi import FastAPI, Request
from src.app.core.database import DatabaseConnection
from src.app.core.redis import RedisConnection
from src.app.core.metrics import metrics


class AppState(TypedDict):
    db: DatabaseConnection
    redis: RedisConnection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    database = DatabaseConnection(
        db_url='postgresql+asyncpg://user:password@localhost:5432/database'
    )
    redis = RedisConnection(
        redis_url='redis://localhost:6379'
    )

    await redis.open_connection()
    redis_status = await redis.check_connection()
    await database.open_connection()
    db_status = await database.check_connection()

    # Обновляем метрики статуса подключений
    # metrics.set_database_status(db_status)
    # metrics.set_redis_status(redis_status)

    app.state.database = database
    app.state.redis = redis

    yield 
    # Закрытие (выполняется после yield)
    await database.close_connection()
    await redis.close_connection()