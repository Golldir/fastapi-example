from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import TypedDict

from fastapi import FastAPI, Request
from src.app.core.database import DatabaseConnection
from src.app.core.redis import RedisConnection


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
    await redis.check_connection()
    await database.open_connection()
    await database.check_connection()

    app.state.database = database
    app.state.redis = redis

    yield 
    # Закрытие (выполняется после yield)
    await database.close_connection()
    await redis.close_connection()