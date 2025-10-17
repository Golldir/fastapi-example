from fastapi import Request
from src.app.core.redis import RedisConnection
from fastapi import Depends


def get_redis_connection(request: Request) -> RedisConnection:
    return request.app.state.redis
