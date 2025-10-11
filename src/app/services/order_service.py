from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.order_repository import OrderRepository
from src.app.models.order_model import Order
from src.app.core.uow import UnitOfWork
from src.app.schemas.order_schema import OrderCreateSchema
from src.app.core.metrics import metrics


class OrderService:
    """Сервис для работы с заказами"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        
    async def get_order(self, order_id: int) -> Optional[Order]:
        """Получить заказ по ID"""
        
        return await self.uow.order_repository.get_order(order_id=order_id)
    
    async def create_order(self, order: OrderCreateSchema) -> Order:
        """Создать заказ"""
        try:
            # user_id_exists = await self.uow.user_repository.get_user(order.user_id)
            # if user_id_exists is None:
            #     raise ValueError("User ID does not exist")

            created_order = await self.uow.order_repository.create_order(
                user_id = order.user_id,
                items = order.items,
                total_amount = 100
            )
            
            # Увеличиваем счетчик созданных заказов
            metrics.increment_orders()
            
            return created_order
            
        except Exception as e:
            # В случае ошибки не увеличиваем счетчик
            raise e
