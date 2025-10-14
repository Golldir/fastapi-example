from src.app.core.uow import UnitOfWork
from src.app.dependencies.uow import get_uow
from src.app.services.order_service import OrderService
from fastapi import Depends


async def get_order_service(
    uow: UnitOfWork = Depends(get_uow)
) -> OrderService:
    return OrderService(uow)