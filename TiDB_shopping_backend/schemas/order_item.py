from pydantic import BaseModel

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(OrderItemBase):
    id: str
    product_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True
