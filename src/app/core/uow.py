from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.interfaces import IUnitOfWork
# from src.app.repositories.user_repository import UserRepository
from src.app.repositories.order_repository import OrderRepository

class UnitOfWork(IUnitOfWork):
    """Unit of Work с ленивой загрузкой репозиториев"""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._repositories: Dict[str, Any] = {}
    
    # @property
    # def users(self) -> UserRepository:
    #     """Получить репозиторий пользователей (создается при первом обращении)"""
    #     if 'users' not in self._repositories:
    #         self._repositories['users'] = UserRepository(self.dbsession)
    #     return self._repositories['users']
    
    @property
    def order_repository(self) -> OrderRepository:
        """Получить репозиторий заказов (создается при первом обращении)"""
        if 'orders_repository' not in self._repositories:
            self._repositories['orders_repository'] = OrderRepository(self.db_session)
        return self._repositories['orders_repository']
    
    async def commit(self) -> None:
        """Зафиксировать транзакцию"""
        await self.db_session.commit()
    
    async def rollback(self) -> None:
        """Откатить транзакцию"""
        await self.db_session.rollback()
    
    async def __aenter__(self) -> "UnitOfWork":
        """Асинхронный контекстный менеджер - вход"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Асинхронный контекстный менеджер - выход"""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.db_session.close()