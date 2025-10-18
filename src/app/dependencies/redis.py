from fastapi import Request
from src.app.core.redis import RedisConnection
from src.app.core.config import settings

def get_redis_connection(request: Request) -> RedisConnection:
    if request and hasattr(request.app.state, 'redis'):
        return request.app.state.redis

