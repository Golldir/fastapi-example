from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

class DatabaseConnection:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.async_engine = None  # Инициализируем как None
        self.async_session = None

    async def get_async_engine(self) -> AsyncEngine:
        return self.async_engine

    async def get_async_session(self) -> AsyncSession:
        return self.async_session

    async def open_connection(self) -> AsyncSession:
        self.async_engine = create_async_engine(self.db_url)
        self.async_session = async_sessionmaker(
            bind=self.async_engine, expire_on_commit=False
        )
    
    async def check_connection(self) -> bool:
        """Проверить подключение к базе данных"""
        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            # print("✅ Подключение к БД успешно установлено")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            return False

    async def close_connection(self) -> None:
        await self.async_engine.dispose()