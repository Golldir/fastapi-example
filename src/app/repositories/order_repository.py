from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.repositories.base_repository import BaseRepository
from src.app.models.order_model import Order, OrderItem, OrderStatus

class OrderRepository(BaseRepository[Order]):
    """Репозиторий для работы с заказами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)
    
    async def get_order(self, order_id: int) -> Optional[Order]:
        """Получить заказ с элементами"""
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
       
    async def create_order(
        self, 
        user_id: int, 
        items: List[dict],
        total_amount: float
    ) -> Order:
        """Создать заказ с элементами"""
        # Создаем заказ
        order = Order(
            user_id=user_id, 
            status=OrderStatus.PENDING, 
            total_amount=total_amount
        )
        self.session.add(order)
        await self.session.flush()  # Получаем ID заказа
        
        # Создаем элементы заказа
        for item_data in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                price=item_data.price
            )
            self.session.add(order_item)
        
        # Загружаем заказ с элементами
        return await self.get_order(order.id)
    
