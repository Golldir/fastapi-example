import redis.asyncio as redis
from typing import Optional


class RedisConnection:
    def __init__(self, redis_url: str):
        self.redis_url=redis_url
        self.redis_client: Optional[redis.Redis] = None

    async def get_client(self) -> redis.Redis:
        return self.redis_client
 
    async def open_connection(self) -> redis.Redis:
        self.redis_client=redis.from_url(self.redis_url)
    
    async def check_connection(self) -> bool:
        try:
            await self.redis_client.ping()                    
            # print("✅ Подключение к Redis успешно установлено")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к Redis: {e}")
            return False

    async def close_connection(self) -> None:
        await self.redis_client.close()
