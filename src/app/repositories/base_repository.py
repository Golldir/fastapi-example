from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import DeclarativeBase

from src.app.core.interfaces import IRepository

T = TypeVar('T', bound=DeclarativeBase)

class BaseRepository(ABC, Generic[T], IRepository[T]):
    """Базовый репозиторий для работы с базой данных"""
    
    def __init__(
        self, 
        session: AsyncSession, 
        model: type[T]
    ):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[T]:
        """Получить сущность по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Получить все сущности с пагинацией"""
        result = await self.session.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def create(self, **kwargs) -> T:
        """Создать новую сущность"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()  # Получаем ID без коммита
        return instance

    async def update(self, id: int, **kwargs) -> Optional[T]:
        """Обновить сущность по ID"""
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> bool:
        """Удалить сущность по ID"""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount > 0

    async def exists(self, **filters) -> bool:
        """Проверить существование сущности по фильтрам"""
        stmt = select(self.model)
        for field, value in filters.items():
            field_obj = getattr(self.model, field)
            stmt = stmt.where(field_obj == value)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None