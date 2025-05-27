from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.product_service import get_bestsellers
from models.product import Product
from schemas.product import ProductOut

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[ProductOut])
def list_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/bestsellers", response_model=list[ProductOut])
def get_top_selling_products(db: Session = Depends(get_db)):
    return get_bestsellers(db)
