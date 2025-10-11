from fastapi import Request
from src.app.core.redis import RedisConnection

def get_redis_connection(request: Request) -> RedisConnection:
    return request.app.state.redis