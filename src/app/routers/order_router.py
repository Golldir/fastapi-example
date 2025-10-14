from fastapi import APIRouter
from src.app.dependencies.services import get_order_service
from src.app.schemas.order_schema import OrderCreateSchema, OrderGetSchema
from src.app.services.order_service import OrderService
from fastapi import Depends, Body, Request


router = APIRouter()

@router.get('/orders/{order_id}')
async def get_orders(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),

):
    return await order_service.get_order(order_id)

@router.post('/orders', response_model=OrderGetSchema, status_code=201)
async def create_order(
    order: OrderCreateSchema = Body(...),
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.create_order(order)