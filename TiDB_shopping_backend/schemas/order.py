from pydantic import BaseModel
from typing import List
from datetime import datetime
from schemas.order_item import OrderItemBase, OrderItemOut

class OrderBase(BaseModel):
    order_number: str
    total_amount: float
    status: str

class OrderOut(OrderBase):
    id: str
    order_date: datetime
    user_id: str
    items: List[OrderItemOut]
    class Config:
        orm_mode = True

class OrderCreationRequest(BaseModel):
    items: List[OrderItemBase]