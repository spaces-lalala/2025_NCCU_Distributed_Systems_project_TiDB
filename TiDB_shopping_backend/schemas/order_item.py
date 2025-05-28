from pydantic import BaseModel

class OrderItemBase(BaseModel):
    product_id: str
    quantity: int

class OrderItemOut(OrderItemBase):
    id: str
    product_name: str
    quantity: int
    price: float

    class Config:
        orm_mode = True
