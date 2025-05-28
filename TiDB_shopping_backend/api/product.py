from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.product_service import get_best_sellers
from schemas.product import ProductOut
from typing import List, Optional

from database import get_db
from models.product import Product
from schemas.product import ProductOut

router = APIRouter(prefix="/product", tags=["products"])

@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/bestsellers", response_model=list[ProductOut])
def read_best_sellers(db: Session = Depends(get_db)):
    return get_best_sellers(db)