from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None
    sold: Optional[int]
    category_name: Optional[str]
    
    class Config:
        from_attributes = True

class ProductDetailOut(ProductOut):
    stock: int
    description: Optional[str]
    
    class Config:
        from_attributes = True

class ErrorDetail(BaseModel):
    detail: str
