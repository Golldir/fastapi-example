from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class OrderItemSchema(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    
class OrderCreateSchema(BaseModel):
    user_id: int
    items: List[OrderItemSchema]

class OrderGetSchema(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime




