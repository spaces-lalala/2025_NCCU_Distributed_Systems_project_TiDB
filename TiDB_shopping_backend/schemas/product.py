from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    id:str
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    class Config:
        orm_mode = True
    class Config:
        orm_mode = True
